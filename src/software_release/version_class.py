from semver import VersionInfo
from .version_bump_type import BumpType


class VersionString:
    def __init__(self, string) -> None:
        self.string = string

    def __str__(self) -> str:
        return self.string

    def __add__(self, bump_type: BumpType):
        return VersionString(str(getattr(VersionInfo.parse(self.string),
            f'bump_{bump_type}')()))
