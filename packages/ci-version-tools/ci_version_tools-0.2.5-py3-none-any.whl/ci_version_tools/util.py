import semver


def make_env_variables(
    version: semver.Version,
    name_prefix: str,
    is_latest: bool = False,
) -> dict:
    variables = {
        f"{name_prefix}_SEMVER": str(version),
        f"{name_prefix}_MAJOR": str(version.major),
        f"{name_prefix}_MINOR": str(version.minor),
        f"{name_prefix}_PATCH": str(version.patch),
        f"{name_prefix}_MAJOR_MINOR": f"{version.major}.{version.minor}",
        f"{name_prefix}_WITHOUT_BUILD_METADATA": str(version.replace(build=None)),
    }

    if version.prerelease is not None:
        variables[f"{name_prefix}_PRE_RELEASE"] = str(version.prerelease)
        variables[f"{name_prefix}_IS_PRE_RELEASE"] = "1"
    else:
        variables[f"{name_prefix}_IS_RELEASE"] = "1"

    if version.build is not None:
        variables[f"{name_prefix}_BUILD_METADATA"] = str(version.build)

    if is_latest and not version.prerelease:
        variables[f"{name_prefix}_IS_LATEST_RELEASE"] = "1"

    return variables


def print_env(variables: dict) -> None:
    for name, value in variables.items():
        print(f"{name}={value}")
