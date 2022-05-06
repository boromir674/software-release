from software_release.nodes.node import Node


@Node.register_as_subclass('get-pull-requests')
class GetPullRequestsNode(Node):

    @classmethod
    def _handle(cls, request):

        BRANCH_WITH_CHANGES = 'release'
        DESTINATION_BRANCH = 'master'

        pull_requests = cls.run(cls.command('get-pull-requests', 
            "boromir674", # owner
            "software-patterns", # repo_name
        ))
        cls.run(cls.command('render', 'pull-requests', pull_requests))
        return pull_requests

    def handle(self, request):
        pull_requests = self._handle(request)
        request.pull_requests = pull_requests
        return super().handle(request)
