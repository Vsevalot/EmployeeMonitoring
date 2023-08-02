_VERSION_INFO = {
    # will be replaced
    "commit_hash": "000000",
    # will be replaced
    "teamcity_build": "0",
    "major_version": "0",
    "minor_version": "0",
    # will be replaced
    "patch_version": "latest",
}


def get_version() -> str:
    return (
        f'{_VERSION_INFO["major_version"]}.'
        f'{_VERSION_INFO["minor_version"]}.'
        f'{_VERSION_INFO["patch_version"]}'
    )
