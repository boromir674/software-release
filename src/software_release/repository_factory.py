import os
from git import Repo
from .repository import Repository
from .repository_interface import RepositoryInterface
from github import Github

class RepositoryFactoryInterface:
    @staticmethod
    def create(directory: str) -> RepositoryInterface:
        raise NotImplementedError


class RepositoryFactory(RepositoryFactoryInterface):

    @staticmethod
    def create(directory: str):
        repo = Repo(directory)
        try:
            url: str = repo.remote().url
            _ = url.split(':')[1].split('/')
            org_name, repo_name = _[0], '.'.join(_[1].split('.')[:-1])
        except ValueError as error:
            print(error)
            url = 'None'
            org_name = 'None'
            repo_name = 'None'
        try:
            github_proxy = Github(os.environ['SOFTWARE_RELEASE_GH_API_TOKEN'])
        except KeyError as error:
            raise MissingGithubTokenError("The SOFTWARE_RELEASE_GH_API_TOKEN environment variable was not found") from error
        return Repository(
            repo.active_branch,
            directory,
            repo,
            org_name,
            repo_name,
            github_proxy,
        )


class MissingGithubTokenError(Exception): pass
