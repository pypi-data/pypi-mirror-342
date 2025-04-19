import argparse
import contextlib
import enum
import importlib.metadata
import logging
import pathlib
import sys

import semver

from . import git, poetry
from .exceptions import (
    AlreadyReleasedElsewhereError,
    CliError,
    ReleaseTagDoesNotExistError,
    TargetAlreadyReleasedError,
    VersionError,
    VersioningError,
    VersionMismatchError,
)
from .util import make_env_variables, print_env

logger = logging.getLogger(__name__)

DEFAULT_GIT_INTERFACE = git.GitCli()


class VersionType(enum.StrEnum):
    FILE = enum.auto()
    POETRY = enum.auto()


# TODO: Support using GitLab API for fetching Git tags to support shallow clones.
def get_all_release_git_tags(
    version_tag_prefix: str, git_interface: git.GitInterface = DEFAULT_GIT_INTERFACE
) -> dict:
    git_releases = {}

    for tag, sha in git_interface.get_tags(version_tag_prefix).items():
        try:
            version = semver.Version.parse(tag.removeprefix(version_tag_prefix))
        except ValueError:
            logger.debug(
                "Git tag %s had the correct prefix %s"
                "but didn't parse as a valid semver",
                tag,
                version_tag_prefix,
            )
            continue

        logger.debug("Found tagged release %s", version)
        git_releases[tag] = {
            "version": version,
            "sha": sha,
        }

    return git_releases


def is_head_at_tag(
    ref: str, git_interface: git.GitInterface = DEFAULT_GIT_INTERFACE
) -> bool:
    # Resolve commit SHA, as it will differ from the tag SHA
    # for annotated tags.
    tag_commit_sha = git_interface.get_commit_sha(ref)
    head_sha = git_interface.get_commit_sha("HEAD")

    return tag_commit_sha == head_sha


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        default="INFO",
    )
    # TODO: Support checking if sub-projects (e.g. in a monorepo), changelog, etc
    # have versions consistent with the primary source of truth.
    parser.add_argument(
        "--version-source-file", type=pathlib.Path, default=pathlib.Path("VERSION")
    )
    parser.add_argument(
        "--version-source-pyproject",
        type=pathlib.Path,
        default=pathlib.Path("pyproject.toml"),
    )
    parser.add_argument(
        "--version-source",
        type=VersionType,
        default=VersionType.FILE,
        choices=[t.value for t in VersionType],
    )
    parser.add_argument("--git-version-tag-prefix", default="v")
    parser.add_argument("--output-var-prefix", default="VERSION")
    # CI_COMMIT_TAG
    parser.add_argument(
        "--git-tag", help="indicates this is a tagged release build (e.g. v1.2.3)"
    )
    parser.add_argument(
        "--no-fail-if-target-release-exists", action="store_true", default=False
    )

    subcommand = parser.add_subparsers(dest="command", required=True)

    subcommand.add_parser("version")

    subcommand.add_parser("env-vars")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(level=args.log_level)

    try:
        if args.command == "version":
            distribution = importlib.metadata.distribution(__package__)
            print(importlib.metadata.version(distribution.metadata["Name"]))

            sys.exit(0)

        if args.version_source == VersionType.FILE:
            with open(args.version_source_file) as f:
                version = semver.Version.parse(f.read().rstrip())
        elif args.version_source == VersionType.POETRY:
            pep440_version = poetry.get_poetry_project_version(
                args.version_source_pyproject
            )
            version = poetry.pep440_to_semver(pep440_version)

        if args.command == "env-vars":
            all_release_git_tags = get_all_release_git_tags(args.git_version_tag_prefix)

            # Tag (release) build, not just a branch build which happens to
            # point at the same SHA as an existing tag.
            if args.git_tag is not None:
                if args.git_tag not in all_release_git_tags:
                    raise ReleaseTagDoesNotExistError(
                        f"Release tag {args.git_tag} does not exist in git."
                    )

                if args.git_tag.startswith(args.git_version_tag_prefix):
                    with contextlib.suppress(ValueError):
                        tag_version = semver.Version.parse(
                            args.git_tag.removeprefix(args.git_version_tag_prefix)
                        )
                else:
                    raise VersionError(
                        f"Git tag {args.git_tag} doesn't start with the "
                        f"{args.git_version_tag_prefix} prefix."
                    )

                # Fail if current version does not match the one specified
                # in the Git tag.
                if version != tag_version:
                    raise VersionMismatchError(
                        f"Project version {version} in does not match the "
                        f"version {tag_version} in the Git tag. "
                    )

            current_version_git_tag = f"v{version}"

            # The current verson has already been released on a different commit.
            # Examples:
            #   - current version == 1.2.3-dev, existing tag == v1.2.3-dev
            #   - current version == 2.0.0, existing tag == v2.0.0
            if current_version_git_tag in all_release_git_tags:
                tag_sha = all_release_git_tags[current_version_git_tag]["sha"]
                if not is_head_at_tag(tag_sha):
                    raise AlreadyReleasedElsewhereError(
                        f"Version {version} has been released on a "
                        "different commit already. Increment the version to "
                        "a next pre-release to fix this error."
                    )

            target_release_version = version.finalize_version()
            target_version_git_tag = f"v{target_release_version}"

            # The current pre-release version has not been released, but it's
            # target was.
            # Examples:
            #   - current version == 1.2.3-dev, existing tag is v1.2.3
            if version.prerelease and target_version_git_tag in all_release_git_tags:
                if args.no_fail_if_target_release_exists:
                    logger.warning(
                        "Version %s targets %s which is already released.",
                        version,
                        target_release_version,
                    )
                else:
                    raise TargetAlreadyReleasedError(
                        f"Version {version} targets {target_release_version} "
                        "which has been released already. Increment the version "
                        "to fix this error."
                    )

            all_released_versions = {
                r["version"] for _, r in all_release_git_tags.items()
            }
            if all_released_versions:
                latest = version >= max(all_released_versions)
            else:
                latest = True

            variables = make_env_variables(
                version,
                name_prefix=args.output_var_prefix,
                is_latest=latest,
            )
            print_env(variables)

    except (CliError, VersionError, VersioningError) as e:
        logger.error(e)
        sys.exit(1)
