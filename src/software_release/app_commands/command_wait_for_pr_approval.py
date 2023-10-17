import os
from time import sleep
from github import Github

from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.pull_request import PullRequests


class AbstractWaitPullRequestApproval(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.wait_for_pr_approval, '__call__', *args)


@CommandClass.register_as_subclass('wait-for-pr-approval')
class WaitPullRequestApproval(AbstractWaitPullRequestApproval):

    @classmethod
    def wait_for_pr_approval(cls, owner, repo_name, pr_number, *request_args):
        try:
            g = Github(os.environ['SOFTWARE_RELEASE_GH_API_TOKEN'])
        except KeyError as error:
            raise MissingGithubTokenError("The SOFTWARE_RELEASE_GH_API_TOKEN environment variable was not found") from error

        repo = g.get_repo(f"{owner}/{repo_name}")

        pr_approved = False
        while not pr_approved:
            pull_requests = PullRequests.from_github_get_pulls(repo.get_pulls('closed'))
            if pr_number in pull_requests:
                pr = pull_requests[pr_number]
                if pr.state == 'closed':
                    break
            sleep(2)
        return True


class MissingGithubTokenError(Exception): pass
