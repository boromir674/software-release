import os
import urllib

from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand


class AbstractGithubReleasesList(BaseCommand):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, cls.get_github_releases, '__call__', *args, **kwargs)


@CommandClass.register_as_subclass('get-github-releases')
class GetGithubReleases(AbstractGithubReleasesList):

    @staticmethod
    def get_github_releases(owner, repo_name, limit: int | None):
        if not 'SOFTWARE_RELEASE_GH_API_TOKEN' in os.environ:
            raise RuntimeError("Please set the SOFTWARE_RELEASE_GH_API_TOKEN environment variable")

        headers = {
            "Authorization": f"Bearer {os.environ['SOFTWARE_RELEASE_GH_API_TOKEN']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        URL = f'https://api.github.com/repos/{owner}/{repo_name}/releases'
        request = urllib.request.Request(URL, data=None, headers=headers, origin_req_host=None, unverifiable=False,
            method='GET')
        response = urllib.request.urlopen(request)
        if response.status != 200:
            raise RuntimeError(f"Error: {response.status} {response.msg}")

        import json
        import typing as t
        releases: t.List = json.loads(str(response.read(), encoding='utf-8'))

        if limit:
            return releases[:limit]
        return releases
