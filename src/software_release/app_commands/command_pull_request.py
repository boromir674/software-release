import os
import re

from github import Github
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand


__all__ = ['PullRequest']


class AbstractPullRequest(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.create_pull_request, '__call__', *args)


@CommandClass.register_as_subclass('pull-request')
class PullRequest(AbstractPullRequest):

    @staticmethod
    def create_pull_request(owner, repo_name, title, description, head_branch, base_branch):

        # using an access token
        g = Github(os.environ['GH_TOKEN'])
        repo = g.get_repo(f"{owner}/{repo_name}")

        lines = list(description.split('\n'))
        prev_line = lines[0]
        for i in range(1, len(lines)):
            line = lines[i]
            if re.match(r'^\^{2,}', line):
                lines[i] = '-' * len(prev_line)
            prev_line = lines[i]

        pr = repo.create_pull(
            title=title,
            body='\n'.join(lines),
            head=head_branch,
            base=base_branch
        )
        return pr


class PullRequestCreationError(Exception): pass
