from software_release.nodes.node import Node


@Node.register_as_subclass('get-pull-requests')
class GetPullRequestsNode(Node):

    @classmethod
    def _handle(cls, request):

        pull_requests = cls.run(cls.command('get-pull-requests',
            request.repository.org_name, # owner, github username
            request.repository.name, # repository name as seen in github
            'open',
        ))
        for x in pull_requests:
            print('PR', x.title, x.state)
            assert hasattr(x, 'base_ref')
            print('BASE_REF', x.base_ref)
        cls.run(cls.command('render', 'pull-requests', pull_requests))
        return pull_requests

    def handle(self, request):
        pull_requests = self._handle(request)
        request.pull_requests = pull_requests
        return super().handle(request)
