import sys
from time import sleep
import click

from .app_commands import *
# @click.argument('content_image')
# @click.argument('style_image')
# @click.option('--iterations', '-it', type=int, default=100, show_default=True)
# @click.option('--location', '-l', type=str, default='.')
@click.command()
def cli():

    from .repository_factory import RepositoryFactory
    from .release_wizard import ReleaseWizard
    REPO_PATH = '/data/repos/software-patterns'

    repo = RepositoryFactory.create(REPO_PATH)

    release_wizard = ReleaseWizard.create(repo, [
        'welcome-to-app',
        'sleep_0.5',
        'welcome-to-wizard-node',
        'active-branch-check',  # if we are NOT on a branch named 'release', exit
        
        'sleep_0.35',
        'determine-new-version',
# pull master branch
        # 'sleep_0.35',
        # 'version-bump',
        # 'sleep_0.35',
        # 'branch-references',

        # 'changelog',

        # 'sleep_0.35',
        # 'push-active-branch',

        # 'sleep_0.35',
        # 'open-pull-request',

        # 'sleep_0.35',
        # 'get-pull-requests',

        # 'wait-for-pr-approval',
        
        'pull-branch-with-releases',  # pull master branch
        # then modify above since we do not checkout master
        'tag-commit-on-branch-with-releases',
        # 'push-tag',
    ])

    release_wizard.run()
