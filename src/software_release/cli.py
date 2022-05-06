import sys
from time import sleep
import click

from .app_commands import *
from .repository_factory import RepositoryFactory
from .release_wizard import ReleaseWizard


@click.option('--path', '-p', 'repo_path', type=str, default='.')
@click.command()
def cli(repo_path: str):

    repo = RepositoryFactory.create(repo_path)

    release_wizard = ReleaseWizard.create(repo, [
        'welcome-to-app',
        'sleep_0.5',

        'welcome-to-wizard-node',
        'active-branch-check',  # if we are NOT on a branch named 'release', exit
        'sleep_0.35',

        'determine-new-version',
        # 'pull-branch-with-releases',  # ie pull master branch
        # 'sleep_0.35',

        # 'version-bump',
        # 'sleep_0.35',

        # 'branch-references',
        'changelog',
        # 'sleep_0.35',

        # 'push-active-branch',

        # 'sleep_0.35',
        # 'open-pull-request',

        # 'sleep_0.35',
        # 'get-pull-requests',

        # 'wait-for-pr-approval',
        
        # 'pull-branch-with-releases',  # pull master branch

        # 'tag-commit-on-branch-with-releases',
        # 'push-tag',
    ])

    release_wizard.run()
