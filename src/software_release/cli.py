from pathlib import Path
import click
from .app_commands import *
from .repository_factory import RepositoryFactory
from .release_wizard_fct import ReleaseWizardFactory


def build_interactive_console_release_wizard(repo, main_branch='main'):
    """Build a Console Release Wizard.

    Prerequisites:
        - environment variable SOFTWARE_RELEASE_GH_API_TOKEN to authenticate with github API
        - your git HEAD should point to a 'release' branch
        - the 'release' branch should have 'tracking information' set up
        - the 'main' should be up-to-date with the remote

    Recommendations:
        - 'release' should have been branched of off 'main' to avoid conflicts on merge

    Args:
        repo ([type]): [description]
        main_branch (str, optional): [description]. Defaults to 'main'.

    Returns:
        [type]: [description]
    """
    return ReleaseWizardFactory.create(repo, [
        'welcome-to-app',
        # 'sleep_0.5',

        'welcome-to-wizard-node',
        # indicate which branch hosts the tagged commits (ie main)
        'set-release-branch_{branch}'.format(branch=main_branch),

        'active-branch-check',  # if we are NOT on a branch named 'release', exit
        # 'sleep_0.35',

        'determine-new-version',
        # 'pull-branch-with-releases',  # ie pull main branch
        # 'sleep_0.35',

        # 'version-bump',  # this modifies pyproject.toml and python files for now

        # 'sleep_0.35',

        # look for documentation files (ie Readme) that contain references to
        # the dev branch and update them so that they point to the 'main' branch
        # 'branch-references',  # TODO fix since the main branch is hard-coded

        'changelog',
        # 'sleep_0.35',

        'push-active-branch',

        # # 'sleep_0.35',
        'open-pull-request',

        # # 'sleep_0.35',
        'get-pull-requests',

        'wait-for-pr-approval',

        # # TODO attempt to push from local main to remote main in case the
        # # merge happened locally first (and then pushed) in contrast to doing
        # # the merge on github (online) through the github web interface

        'pull-branch-with-releases',  # pull main branch

        'tag-commit-on-branch-with-releases',
        'push-tag',

        # # Upload built assets (ie wheels, tar.gz with source distribution)
        # # 1. make a github "release" from the tag created above
        # 'make-gh-release',

        # # 2. make a pypi "release", building a wheel
        # 'publish-in-pypi',
    ])



@click.command()
@click.option('--path', '-p', 'repo_path', default='.', type=str, show_default=True)
@click.option('--config', '-c', 'config_file',
    type=click.Path(exists=False, file_okay=True, readable=True),
    # default=None,
    # show_default=True,
    help="The path to the YAML configuration file that defines the Release Wizard Steps."
)
@click.option('--changelog', '-cl', default=False, is_flag=True, show_default=True,
    help="Just show the computed Changelog Diff")
@click.option('--main-branch', '-mb', default='main', show_default=True, help="The Default Branch, where the tags are expected to be found.")
def cli(repo_path: str, config_file, changelog: bool, main_branch: str):
    print(repo_path)
    repo = RepositoryFactory.create(repo_path)

    if changelog:  # show the automatically generated changelog addition (diff)
        def build_changelog_diff_wizard():
            return ReleaseWizardFactory.create(repo, [
                # indicate which branch hosts the tagged commits (ie main)
                'set-release-branch_{branch}'.format(branch=main_branch),
                
                ## GENERATE CHANGELOG ##
                'prev-version', # determine the previous version released
                'determine-new-version',
                'changelog',  # requires prev-version & determine-new-version
            ])
        release_wizard = build_changelog_diff_wizard()
    else:
        config = Path(config_file)
        if config.exists():
            release_wizard = ReleaseWizardFactory.from_yaml(repo, config_file)
        else:
            release_wizard = build_interactive_console_release_wizard(repo, main_branch=main_branch)


    release_wizard.run()
