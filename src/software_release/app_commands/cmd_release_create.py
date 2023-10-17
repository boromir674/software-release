import typing as t
import os
import urllib

from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand


class AbstractGithubReleaseCreate(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.create_new_github_release, '__call__', *args)


@CommandClass.register_as_subclass('create-github-release')
class CreateGithubRelease(AbstractGithubReleaseCreate):

    @staticmethod
    def create_new_github_release(release_info: t.Dict[str, str | bool]):
        if not 'SOFTWARE_RELEASE_GH_API_TOKEN' in os.environ:
            raise RuntimeError("Please set the SOFTWARE_RELEASE_GH_API_TOKEN environment variable")

        import urllib.parse
        params = urllib.parse.urlencode(release_info
        # {
        #     "tag_name": "v1.0.0",
        #     "target_commitish": "master",
        #     "name": "v1.0.0",
        #     "body":"Description of the release",
        #     "draft": False,
        #     "prerelease": True,
        #     "generate_release_notes": False
        # }
        )
        headers = {
            "Authorization": f"Bearer {os.environ['SOFTWARE_RELEASE_GH_API_TOKEN']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        URL = f'https://api.github.com/repos/{owner}/{repo_name}/releases'
        request = urllib.request.Request(URL, data=None, headers=headers, origin_req_host=None, unverifiable=False,
            method='POST')
        response = urllib.request.urlopen(request)
        if response.status != 200:
            raise RuntimeError(f"Error: {response.status} {response.msg}")

        import json
        import typing as t
        releases: t.List = json.loads(str(response.read(), encoding='utf-8'))
        return releases
        # import datetime
        # for release_dict in releases:
        #     try:
        #         # read release published at date and keep only YYYY-MM-DD
        #         release_published_at = datetime.datetime.strptime(release_dict['published_at'], '%Y-%m-%dT%H:%M:%SZ').date()
        #         print(f"ID: {release_dict['id']} - {release_dict['name']} - Published: {release_published_at} - is pre-release: {release_dict['prerelease']}")
        #     except KeyError as e:
        #         print(e)
        #         print(f'[DEBUG]: Available Keys: {release_dict.keys()}')
