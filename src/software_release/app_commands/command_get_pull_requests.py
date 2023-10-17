import os

from github import Github

from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.pull_request import PullRequests


class AbstractGetPullRequest(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.get_pull_requests, '__call__', *args)


@CommandClass.register_as_subclass('get-pull-requests')
class GetPullRequests(AbstractGetPullRequest):

    @staticmethod
    def get_pull_requests(owner, repo_name, *request_args):
        # By default GETs only the open pull requests
        if not request_args:
            # overide the default from open to all
            args = ['all']
        else:
            args = request_args
        try:
            g = Github(os.environ['SOFTWARE_RELEASE_GH_API_TOKEN'])
        except KeyError as error:
            raise MissingGithubTokenError("The SOFTWARE_RELEASE_GH_API_TOKEN environment variable was not found") from error
        repo = g.get_repo(f"{owner}/{repo_name}")
        pull_requests = repo.get_pulls(*args)
        return PullRequests.from_github_get_pulls(pull_requests)

class MissingGithubTokenError(Exception): pass
