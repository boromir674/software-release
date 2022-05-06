from git import Repo
from .repository import Repository
from .repository_interface import RepositoryInterface


class RepositoryFactoryInterface:
    @staticmethod
    def create(directory: str) -> RepositoryInterface:
        raise NotImplementedError


class RepositoryFactory(RepositoryFactoryInterface):

    @staticmethod
    def create(directory: str):
        repo = Repo(directory)
        return Repository(
            repo.active_branch,
            directory,
            repo
        )
