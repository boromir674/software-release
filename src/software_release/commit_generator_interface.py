from abc import ABC
from typing import Iterator
from .repository_interface import RepositoryInterface
from software_release.commit_interface import CommitInterface


class CommitGeneratorInterface(ABC):

    def generate_commits(
        self,
        repository: RepositoryInterface,
        revision: str) -> Iterator[CommitInterface]:
        raise NotImplementedError
