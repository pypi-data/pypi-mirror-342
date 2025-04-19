import pathlib

import packaging.version
import semver
import tomllib

from .exceptions import VersionError


def pep440_to_semver(pep440_version: packaging.version.Version) -> semver.Version:
    if pep440_version.epoch != 0:
        raise VersionError("PEP440 versions with epoch cannot be converted to semver")
    if pep440_version.post is not None:
        raise VersionError("PEP440 versions with post cannot be converted to semver")
    if len(pep440_version.release) > 3:
        raise VersionError(
            "PEP440 versions with more than 3 release segments "
            "cannot be converted to semver"
        )

    major = pep440_version.release[0]

    minor = pep440_version.release[1] if len(pep440_version.release) >= 2 else 0

    patch = pep440_version.release[2] if len(pep440_version.release) >= 3 else 0

    pre_release_parts = []

    if pep440_version.dev is not None:
        pre_release_parts.append(str(pep440_version.dev))

    if pep440_version.pre is not None:
        pre_type, pre_nr = pep440_version.pre

        type_map = {
            "a": "alpha",
            "b": "beta",
            "rc": "rc",
        }
        pre_release_parts.extend((type_map[pre_type], str(pre_nr)))

    prerelease = ".".join(pre_release_parts) if pre_release_parts else None

    return semver.Version(major=major, minor=minor, patch=patch, prerelease=prerelease)


def get_poetry_project_version(
    pyproject_path: pathlib.Path,
) -> packaging.version.Version:
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    return packaging.version.Version(pyproject["tool"]["poetry"]["version"])
