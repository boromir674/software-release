import typing as t
from software_release.nodes.node import Node


@Node.register_as_subclass('make-gh-release')
class MakeGithubRelease(Node):

    @classmethod
    def _handle(cls, request):

        github_releases: t.List[t.Dict[str, t.Any]] = cls.cmd('get-github-releases',
            request.repository.org_name, # owner, github username
            request.repository.name, # repository name as seen in github
            limit=3,
        )
        # print(f"Github Releases: {github_releases}")
        cls.cmd('render', 'github-releases-list', github_releases)
        is_prerelease = request.new_version.is_prerelease()
        print(f"[DEBUG] is prerelase ? {is_prerelease}")

        tag_str = request.tag_reference.name
        # tag_str = "v1.3.1-dev"

        # Ask user if Release is Draft
        dialog = cls.dialog('select-gh-release-info')
        is_draft: bool = dialog.dialog({
            'options': [
                'Is DRAFT',
                'is NOT Draft',
        ]}) == 'Is DRAFT'

        cls.cmd('create-github-release', {
            "tag_name": request.tag_reference.name,
            # "target_commitish": "main",
            "name": f"{request.repository.name} {tag_str} Release",
            # "body": "Description of the release",
            "draft": is_draft,
            "prerelease": is_prerelease,
            "generate_release_notes": True,
        })

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
