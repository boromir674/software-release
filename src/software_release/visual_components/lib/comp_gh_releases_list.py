import typing as t
from collections import OrderedDict
import datetime
from functools import reduce
from attr import define, field

from ..visual_component import VisualComponent

class GithubReleaseProtocol(t.Protocol):
    id: int
    name: str
    published_at: str


@VisualComponent.register_as_subclass('github-releases-list')
@define
class GithubReleasesTable(VisualComponent):
    github_releases: t.List[t.Dict]
    
    _max_col_lens: t.List[int] = field(init=False)

    COLUMNS = ['name', 'published_at', 'prerelease']
    extractors = {
        'name': lambda x: x['name'],
        'published_at': lambda x: str(datetime.datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%SZ').date()),
        'prerelease': lambda x: str(x['prerelease']),
    }

    def __attrs_post_init__(self):
        c =                 [tuple([self.extractors[x](gh_rel) for x in self.COLUMNS]
                    # gh_rel['name'],
                    # datetime.datetime.strptime(gh_rel['published_at'], '%Y-%m-%dT%H:%M:%SZ').date(),
                    # gh_rel['prerelease']
                ) for gh_rel in self.github_releases] + [tuple(self.COLUMNS)]
        print(c)
        i = reduce(
                lambda i, j: (
                    i[0] if len(str(i[0])) > len(str(j[0])) else j[0],
                    i[1] if len(str(i[1])) > len(str(j[1])) else j[1],
                    i[2] if len(str(i[2])) > len(str(j[2])) else j[2],
                ),
                [tuple([self.extractors[x](gh_rel) for x in self.COLUMNS]
                    # gh_rel['name'],
                    # datetime.datetime.strptime(gh_rel['published_at'], '%Y-%m-%dT%H:%M:%SZ').date(),
                    # gh_rel['prerelease']
                ) for gh_rel in self.github_releases] + [tuple(self.COLUMNS)]
                # [(
                #     gh_rel['name'],
                #     datetime.datetime.strptime(gh_rel['published_at'], '%Y-%m-%dT%H:%M:%SZ').date(),
                #     gh_rel['prerelease']
                # ) for gh_rel in self.github_releases]
            )
        assert type(i) == tuple
        print(i)
        r = [len(str(x)) for x in i]
        self._max_col_lens = r
        # self._max_col_lens = list(map(
        #     lambda x: len(str(x)),
        #     reduce(
        #         lambda i, j: (
        #             i[0] if len(str(i[0])) > len(str(j[0])) else j[0],
        #             i[1] if len(str(i[1])) > len(str(j[1])) else j[1],
        #             i[2] if len(str(i[2])) > len(str(j[2])) else j[2],
        #         ),
        #         [tuple([self.extractors[x](gh_rel) for x in self.COLUMNS]
        #             # gh_rel['name'],
        #             # datetime.datetime.strptime(gh_rel['published_at'], '%Y-%m-%dT%H:%M:%SZ').date(),
        #             # gh_rel['prerelease']
        #         ) for gh_rel in self.github_releases] + [tuple(self.COLUMNS)]
        #         # [(
        #         #     gh_rel['name'],
        #         #     datetime.datetime.strptime(gh_rel['published_at'], '%Y-%m-%dT%H:%M:%SZ').date(),
        #         #     gh_rel['prerelease']
        #         # ) for gh_rel in self.github_releases]
        #     )
        # ))

    def render(self):
        return [
            self.render_header(),
            self.render_body(),
            # f'\nGIT PUSH: Pushed Tag \'{self.tag_name}\' to remote \'{self.remote_slug}\' !\n\n',
        ]

    def render_header(self):
        return self.render_row(self.COLUMNS)
    
    def render_body(self):
        return '\n'.join([self.render_row(
            tuple([self.extractors[x](gh_rel) for x in self.COLUMNS])
        ) for gh_rel in self.github_releases])
    
    def render_row(self, row):
        return '|'.join(list(map(lambda x: x[0] + x[1] + x[0], zip(
            [' ', ' ', ' '],
            row,
            [' ' * (self._max_col_lens[i] - len(row[i])) for i in range(len(row))]
        )))) + '\n'
