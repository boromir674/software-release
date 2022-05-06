from software_release.nodes.node import Node
from software_release.pull_request import PullRequest


@Node.register_as_subclass('open-pull-request')
class OpenPullRequestNode(Node):

    @classmethod
    def _handle(cls, request):

        BRANCH_WITH_CHANGES = 'release'
        DESTINATION_BRANCH = 'temp'

        command = cls.command('pull-request', 
            "boromir674", # owner
            "software-patterns", # repo_name
            f"Software Patterns v{request.new_version} Release", # title
            request.changelog_additions, # description
            BRANCH_WITH_CHANGES, # head_branch, where our changes are implemented
            DESTINATION_BRANCH, # base_branch, where we want to merge to
        )
        pull_request = cls.run(command)

        command = cls.command('render', 'created-pull-request',
            pull_request.number,
            pull_request.url,
            pull_request.html_url,
            BRANCH_WITH_CHANGES,
            DESTINATION_BRANCH
        )
        cls.run(command)
        return pull_request

    def handle(self, request):
        pull_request = self._handle(request)
        request.pull_request = PullRequest.from_github_pull_request(pull_request)
        return super().handle(request)
