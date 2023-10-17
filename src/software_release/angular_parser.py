"""Provides a Commit Parser following the Angular Style Specification.

https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines
"""
import typing as t
import logging
import re
from typing import List
from collections import namedtuple, OrderedDict

logger = logging.getLogger(__name__)


re_breaking = re.compile("BREAKING[ -]CHANGE: (.*)")


ParsedCommit = namedtuple(
    "ParsedCommit", ["bump", "type", "scope", "descriptions"]
)


def parse_paragraphs(text: str) -> List[str]:
    """
    This will take a text block and return a tuple containing each
    paragraph with single line breaks collapsed into spaces.

    :param text: The text string to be divided.
    :return: A tuple of paragraphs.
    """
    return [
        paragraph.replace("\n", " ")
        for paragraph in text.split("\n\n")
        if len(paragraph) > 0
    ]


# Supported commit types for parsing
TYPES = OrderedDict((  # alias (on git message) -> human readable label 
    ('feat', 'feature'),
    ('fix', 'fix'),
    ('test', 'test'),
    ('docs', 'documentation'),
    ('dev', 'development'),
    ('style', 'style'),
    ('refactor', 'refactor'),
    ('build', 'build'),
    ('ci', 'ci'),
    ('perf', 'performance'),
    ('chore', 'chore'),
    ('revert', 'revert'),
    ('improvement', 'improvement'),

    ('dev-container', 'dev-container'),
    # frontend specific
    ('storybook', 'storybook'),

))

regex_components = (
    r"(?:\((?P<scope>[^\n]+)\))?"
    r"(?P<break>!)?: "
    r"(?P<subject>[^\n]+)"
    r"(:?\n\n(?P<text>.+))?"
)

MINOR_TYPES = [
    "feat",
]

PATCH_TYPES = [
    "fix",
    "perf",
]


def parse_commit_message(message: str, strict=False) -> ParsedCommit:
    """Parse a commit message according to the angular commit guidelines specification.

    https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines

    Determines the minimum version bump that should be applied, judging
    by examining the successfully parsed commit messages.

    Args:
        message (str): The commit message to parse.
        strict (bool): If True, parse only messages if their 'type' is known to the precompiled list of TYPES.
    
    Returns:
        ParsedCommit: A tuple containing the minimum version bump, the type of
            the commit, the scope of the commit, and the description of the
            commit.
    
    Raises:
        UnknownCommitMessageStyleError: if regular expression match fails
    """
    types: t.List[str] = list(TYPES.keys())
    if not strict:
        types.append('\w[\w\-_]*')
    re_parser = re.compile(
        r"(?P<type>" + "|".join(types) + ")"
        r"(?:\((?P<scope>[^\n]+)\))?"
        r"(?P<break>!)?: "
        r"(?P<subject>[^\n]+)"
        r"(:?\n\n(?P<text>.+))?",
        re.DOTALL,  # make dot match newline
    )
    # Attempt to parse the commit message with a regular expression
    parsed = re_parser.match(message)
    if not parsed:
        raise UnknownCommitMessageStyleError(
            "Unable to parse the given commit message: {}".format(message)
        )

    # descriptions have 1 or more elements: 1st being subject and each of the
    # rest correspond to a text paragraph
    descriptions_list: List[str] = [parsed.group("subject")]
    if parsed.group("text"):
        descriptions_list.extend(list(parse_paragraphs(parsed.group("text"))))

    # Check for mention of breaking changes
    commit_change_type = parsed.group("type")
    level_bump = 0
    if parsed.group("break") or any([re_breaking.match(p) for p in descriptions_list]):
        level_bump = 3  # Major
    # Set the bump level based on commit type
    elif commit_change_type in MINOR_TYPES:
        level_bump = max([level_bump, 2])
    elif commit_change_type in PATCH_TYPES:
        level_bump = max([level_bump, 1])

    return ParsedCommit(
        level_bump,
        TYPES.get(commit_change_type, commit_change_type),
        parsed.group("scope"),
        descriptions_list,
    )


class UnknownCommitMessageStyleError(Exception): pass
