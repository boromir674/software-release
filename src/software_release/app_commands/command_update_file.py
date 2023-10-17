from typing import Tuple, List
import typing as t
import re
import json
import logging
from collections import OrderedDict
from software_release.commands.command_class import CommandClass
from software_release.repository_interface import RepositoryInterface
from software_release.config_reader import config
from software_release.angular_parser import (
    parse_commit_message,
    UnknownCommitMessageStyleError,
    TYPES as supported_change_types,
)
from software_release.commit_generator import BranchCommitsGenerator

from .abstract_command_update_file import AbstractUpdateFilesCommand


logger = logging.getLogger(__name__)

RegExPair = Tuple[str, str]

RegExPairs = Tuple[RegExPair]

FileRegexes = Tuple[RegExPairs]


__all__ = ['UpdateVersionStringCommand', 'UpdateBranchReferencesCommand',
    'UpdateChangelogCommand']


# SEMVER_REGEX: str
# try:
#     from semantic_version_check import regex
#     regex_pattern: t.Pattern = regex
#     SEMVER_REGEX = regex.pattern
# except ImportError:
SEMVER_REGEX = (
    r'^(?:?P<major>0|[1-9]\d*)'
    r'\.'
    r'(?:?P<minor>0|[1-9]\d*)'
    r'\.'
    r'(?:?P<patch>0|[1-9]\d*)'
    r'(?:-'
    r'(?:?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+'
    r'(?:?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)
SEMVER_REGEX = (
    r'^(?:?P<major>0|[1-9]\d*)'
    r'\.'
    r'(?:?P<minor>0|[1-9]\d*)'
    r'\.'
    r'(?:?P<patch>0|[1-9]\d*)'
)
SEMVER_REGEX = r'\d+\.\d+\.\d+'


# from semantic_version_check import regex


# SEMVER_REGEX: str = regex.pattern


@CommandClass.register_as_subclass('update-version-string')
class UpdateVersionStringCommand(AbstractUpdateFilesCommand):

    def __new__(cls, repository: RepositoryInterface, current_version, new_version: str):
        file_path = cls.file_path(repository.directory_path)
        repo_config = config(repository.directory_path)

        files = [
            file_path('setup.cfg'),
            file_path('README.rst'),
            file_path('pyproject.toml'),
            file_path('docs', 'conf.py'),
            file_path('package.json'),
        ]
        regexes = [
            # setup.cfg
            (
                (  # 1st substitution
                    fr'(version\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
                (  # 2nd substitution
                    r'(download_url\s*=\s*https://github.com/{username}/{repo}/archive/v){prev_version}(.tar.gz)'.format(
                        username=repository.org_name, repo=repository.name, prev_version=current_version),
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
            # README.rst
            (
                (  # 1st substitution
                    fr'(["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
            # pyproject.toml
            (
                (
                    fr'(version\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
            # docs/conf.py version='0.0.1'
            (
                (
                    fr'(release\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
                (
                    fr'(version\s*=\s*["\']?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
            # package.json
            (
                (
                    fr'((?:  |    )"version": "v?){current_version}(")',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
        ]
        # optional python file; ie package_name/src/__init__.py, __version__.py
        if 'version_variable' in repo_config['software_release']:
            version_file_path, version_variable_name = repo_config['software_release']['version_variable'].split(':')
            files.append(file_path(*list(version_file_path.split('/'))))
            regexes.append((
                (
                    fr'({version_variable_name}\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ))
        else:
            logger.debug("Section [software-release] not found in pyproject.toml")
        cmd_instance = super().__new__(cls, files, regexes)
        return cmd_instance


@CommandClass.register_as_subclass('update-branch-refs')
class UpdateBranchReferencesCommand(AbstractUpdateFilesCommand):

    def __new__(cls, repository: RepositoryInterface, branch_name):
        file_path = cls.file_path(repository.directory_path)

        files = [
            file_path('README.rst'),
        ]
        regexes = [
            # README.rst
            (
                (
                    fr'(compare/v{SEMVER_REGEX}\.\.\.?)([\w\-_\d]+)',
                    fr"\g<1>{branch_name}"
                ),
            ),
        ]

        cmd_instance = super().__new__(cls, files, regexes)
        return cmd_instance


re_breaking = re.compile('BREAKING CHANGES?:\s*(.*)')


def my_get_changelog(commit_generator) -> dict:
    """
    Generates a changelog from given version till HEAD.\n
    :param from_version: The last version not in the changelog. The changelog
                         will be generated from the commit after this one.
    :return: a dict with different changelog sections
    """
    # changes: dict = {
    #     'breaking': [],
    # }
#     ('style', 'style'),
#     ('chore', 'chore'),
#     ('revert', 'revert'),

    changes = OrderedDict([
        (change_type, []) for change_type in supported_change_types.values()
    ] + [('breaking', [])])

    for commit in iter(commit_generator):
        try:
            # [level_bump [3,2,1], type [feature, fix, etc], 'scope', 'subject']
            # ["bump", "type", "scope", "descriptions"]
            message = parse_commit_message(commit.message)
            # if message[1] not in changes:
            #     continue
            commit_semantic_type: str = message.type  # ie feat, test, fix, etc
            descriptions: List[str] = message.descriptions
            commit_subject: str = descriptions[0]  # commit subject after type and optional scope
            if commit_semantic_type not in changes:
                changes[commit_semantic_type] = []    
            changes[commit_semantic_type].append((commit.sha, commit_subject))

            if len(descriptions) > 1:
                if 'BREAKING CHANGE' in descriptions[1]:
                    parts = re_breaking.match(descriptions[1])
                    if parts:
                        changes['breaking'].append((commit.sha, parts.group(1)))
                if len(descriptions) > 2:
                    if descriptions[2] and 'BREAKING CHANGE' in descriptions[2]:
                        parts = re_breaking.match(descriptions[2])
                        if parts:
                            changes['breaking'].append((commit.sha, parts.group(1)))

        except UnknownCommitMessageStyleError as err:
            print(err)
            pass

    return changes


def rst_changelog(new_version: str, changelog: dict, date: str = None, header: bool = False) -> str:
    """
    Generates an rst version of the changelog.
    :param str new_version: A string with the version number.
    :param dict changelog: A dict holding the items per section from generate_changelog.
    :param bool header: A boolean that decides whether a changes subsection should be included or not.
    :param str date: an optional date to include in subsection generated along with the version
    :return: The rst formatted changelog.
    """
    changelog_entry_undeline_char = '='
    if new_version[0] == 'v':
        new_version = new_version[1:]
    b = new_version
    if date:
        b += f' ({date})'
    b += '\n{underline}'.format(
        underline=changelog_entry_undeline_char * len(b)
    )

    if header:
        CHANGES_SUBSECTION = 'Changes'
        changes_underline_char = '^'
        b += '\n\n{changes_title}\n{underline}'.format(
            changes_title=CHANGES_SUBSECTION,
            underline=changes_underline_char * len(CHANGES_SUBSECTION)
        )
    change_category_underline_char = '"'
    b += '\n\n' + '\n\n'.join(
        [changes_item(
            header=f'{change_type}\n{len(change_type) * change_category_underline_char}',
            body=changes_to_string(changes),
        ) for change_type, changes in changelog.items() if changes])

    return b.strip()

def md_changelog(new_version: str, changelog: dict, date: str = None, header: bool = False) -> str:
    """Generate a markdown formated updated changelog."""
    if new_version[0] == 'v':
        new_version = new_version[1:]
    b = new_version
    if date:
        b += f' ({date})'
    b = '## ' + b
    
    item_section_level = '####'
    if header:
        CHANGES_SUBSECTION = 'Changes'
        b += '\n\n### {changes_title}'.format(
            changes_title=CHANGES_SUBSECTION,
        )
        item_section_level += '#'
    b += '\n\n' + '\n\n'.join(
        [changes_item(
            header=f'{item_section_level} {change_type}',
            body=changes_to_string(changes),
        ) for change_type, changes in changelog.items() if changes])

    return b.strip()


def changes_to_string(changes: t.Sequence[t.Tuple[str, str]]) -> str:
    return '\n'.join('- {change_item}'.format(
        change_item=message) for _commit_hash, message in changes)


def changes_item(header: str, body: str) -> str:
    return '{header}\n{body}'.format(header=header, body=body)


@CommandClass.register_as_subclass('update-changelog')
class UpdateChangelogCommand(AbstractUpdateFilesCommand):

    SECTION = 'Changelog'
    SECTION_DIRECTIVE = '=' * len(SECTION)
    supported_changelog_formats = {
        'rst': 'CHANGELOG.rst',
        'md': 'CHANGELOG.md',
    }

    default_changelog_file = 'CHANGELOG.rst'

    def __new__(cls, repository: RepositoryInterface, current_version, new_version, date):
        latest_version_string_in_changelog = str(current_version)
        if bool(current_version):
            current_version = f'v{current_version}'
        file_path = cls.file_path(repository.directory_path)

        changelog_dict = my_get_changelog(BranchCommitsGenerator(repository, current_version))
        changelog_rst_string = rst_changelog(str(new_version), changelog_dict, date, header=True)
        changelog_md_string = md_changelog(str(new_version), changelog_dict, date, header=True)
        if not changelog_rst_string or not changelog_md_string:
            logger.error("No Changelog Content Generated: %s", json.dumps({
                'changelog_item_types': '[' + ', '.join([str(x) for x in changelog_dict.keys()]) + ']',
                'changelog_rst_string': changelog_rst_string,
                'changelog_md_string': changelog_md_string,
            }))

        files = [
            file_path(cls.supported_changelog_formats['rst']),
            file_path(cls.supported_changelog_formats['md']),
        ]
        regexes = [
            # CHANGELOG.rst
            (
                (  # 1st replacement operation
                    fr'({cls.SECTION}\n{cls.SECTION_DIRECTIVE}\n*)(v?{latest_version_string_in_changelog})',
                    fr'\g<1>{changelog_rst_string}\n\n\n\g<2>'
                ),
            ),
            # CHANGELOG.md
            (
                (  # 1st replacement operation
                    fr'(# Changelog\n+)(## \[?v?{latest_version_string_in_changelog}\]?)',
                    fr'\g<1>{changelog_md_string}\n\n\n\g<2>'
                    # fr'\n## [{new_version}] - {date}'
                ),
            ),
        ]

            # # CHANGELOG.md
            #     (
            #         fr'({cls.SECTION}\n{cls.SECTION_DIRECTIVE}\n*)(v?{latest_version_string_in_changelog})',
            #         fr'\g<1>{changelog_rst_string}\n\n\n\g<2>'
            #     ),
        cmd_instance = super().__new__(cls, files, regexes)
        cmd_instance.changes_added = changelog_rst_string
        return cmd_instance

    def execute(self) -> None:
        files_changed = super().execute()
        return files_changed, self.changes_added
