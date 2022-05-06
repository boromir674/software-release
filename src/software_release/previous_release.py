import re
from typing import Optional

import attr
from git import TagObject


class PreviousReleasedVersionComputerInterface:

    def compute_previous_release(self, repository):
        raise NotImplementedError


@attr.s
class PreviousReleased(PreviousReleasedVersionComputerInterface):
    revision: attr.ib()

    def compute_previous_release(self, repository):
        previous_release = get_current_version_by_tag(repository.repo_proxy)
        return previous_release


def get_last_version(repo, skip_tags=None) -> Optional[str]:
    """Find the latest version relesed by scanning the repo tags.

    The repo tags need to start with v;

    Example: v1.0.0, v0.5.1, etc

    :return: A string containing a version number.
    """
    skip_tags = skip_tags or []

    def version_finder(tag):
        if isinstance(tag.commit, TagObject):
            return tag.tag.tagged_date
        return tag.commit.committed_date

    for i in sorted(repo.tags, reverse=True, key=version_finder):
        if re.match(r"v\d+\.\d+\.\d+", i.name):  # Matches vX.X.X
            if i.name in skip_tags:
                continue
            return i.name[1:]  # Strip off 'v'


def get_current_version_by_tag(repo, skip_tags=None) -> str:
    """
    Find the current version of the package in the current working directory using git tags.

    :return: A string with the version number or 0.0.0 on failure.
    """
    version = get_last_version(repo, skip_tags=None)
    if version:
        return version
    return "0.0.0"
