import re
from typing import Tuple
import logging
from software_release.commands.base_command import BaseCommand

__all__ = ['AbstractUpdateFilesCommand']


RegExPair = Tuple[str, str]

RegExPairs = Tuple[RegExPair]

FileRegexes = Tuple[RegExPairs]

logger = logging.getLogger(__name__)


class AbstractUpdateFilesCommand(BaseCommand):

    def __new__(cls, files: Tuple[str], regexes: FileRegexes):
        return super().__new__(cls, re, 'sub', files, regexes)

    def execute(self):
        return list(filter(None, [self.update_file(file_path, regex_pairs)
            for file_path, regex_pairs in zip(self.args[0], self.args[1])]))

    def update_file(self, file_path: str, regex_pairs: RegExPairs):
        with open(file_path, mode='r') as fr:
            initial_content = fr.read()

        content = str(initial_content)
        for match_regex, replace_regex in regex_pairs:
            content = re.sub(match_regex, replace_regex, content)

        file_content_changed = content != initial_content
        print(file_content_changed)
        assert file_content_changed

        if file_content_changed:
            with open(file_path, mode='w') as fw:
                fw.write(content)
            return file_path

    @classmethod
    def file_path(cls, repository_root_path):
        def _file_path(*paths):
            return os.path.join(repository_root_path, *paths)
        return _file_path