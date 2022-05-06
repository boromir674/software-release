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
        url: str = repo.remote().url
        _ = url.split(':')[1].split('/')
        org_name, repo_name = _[0], _[1].split('.')[0]
        return Repository(
            repo.active_branch,
            directory,
            repo,
            org_name,
            repo_name,
        )
