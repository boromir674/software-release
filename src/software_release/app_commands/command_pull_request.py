import os
import re

from github import Github
from github.GithubException import GithubException, UnknownObjectException
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.pull_request import PullRequest
import logging
import json

__all__ = ['OpenPullRequest']

logger = logging.getLogger(__name__)


class AbstractPullRequest(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.create_pull_request, '__call__', *args)


@CommandClass.register_as_subclass('pull-request')
class OpenPullRequest(AbstractPullRequest):

    @staticmethod
    def create_pull_request(owner, repo_name, title, description, head_branch, base_branch):

        # using an access token
        try:
            g = Github(os.environ['SOFTWARE_RELEASE_GH_API_TOKEN'])
        except KeyError as error:
            raise MissingGithubTokenError("The SOFTWARE_RELEASE_GH_API_TOKEN environment variable was not found") from error
        try:
            repo_path = f"{owner}/{repo_name}"
            repo = g.get_repo(repo_path)
        except UnknownObjectException as error:
            logger.debug("Repository not found: %s", json.dumps({
                'owner': str(owner),
                'repo_name': repo_name,
                'repository_path': repo_path,
                'error': str(error),
            }, indent=4, sort_keys=True))
            raise error

        lines = list(description.split('\n'))
        prev_line = lines[0]
        for i in range(1, len(lines)):
            line = lines[i]
            if re.match(r'^\^{2,}', line):
                lines[i] = '-' * len(prev_line)
            prev_line = lines[i]

        try:
            pr = repo.create_pull(
                title=title,
                body='\n'.join(lines),
                # the branch with the updates; FROM (ie release branch)
                head=str(head_branch),
                # where to merge the updates: TO (ie main branch)
                base=str(base_branch)
            )
        except GithubException as error:
            logger.debug("Failed to open PR: %s", json.dumps({
                'title': title,
                'head': str(head_branch),  # the branch with the updates; FROM (ie release branch)
                'base': str(base_branch),  # where to merge the updates: TO  (ie main branch)
            }, indent=4, sort_keys=True))
            raise PullRequestCreationError("Failed to create a new Pull Request"
            " on github.com! Could be that there is an already opened PR,"
            " with the same 'from' and 'to' branches, or that the 'base") from error
        return PullRequest.from_github_pull_request(pr)


class PullRequestCreationError(Exception): pass

class MissingGithubTokenError(Exception): pass
