from datetime import date

from software_release.nodes.node import Node

import logging

logger = logging.getLogger(__name__)


@Node.register_as_subclass('changelog')
class UpdateChangelogNode(Node):

    @classmethod
    def _handle(cls, request):
        changed_files, changes_added = cls.cmd('update-changelog',
            request.repository,
            request.previous_version,
            request.new_version,
            date.today().strftime('%Y-%m-%d'))
        print(type(changed_files))
        print(changed_files)
        print(changes_added)
        if changed_files:
            [changelog_file] = changed_files
            cls.echo('We are about to commit the Changelog file.\n'
            'Please make any adjustments, save them and proceed.\n'
            f' Changelog: {changelog_file}')
            interactive = True
            if interactive:
                cls.dialog('press-enter-to-continue').dialog(None)
            cls.cmd('render', 'updated-changelog',
                    request.repository.directory_path, changelog_file, changes_added)

            commit = cls.cmd('commit-changes',
                request.repository,
                f'docs: update changelog with the release\'s changes')

            cls.cmd('render', 'commited-files',
                    request.repository.directory_path,
                    [changelog_file],
                    commit.message,
                    commit.sha)
        request.changelog_additions = changes_added

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
