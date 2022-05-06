from software_release.nodes.node import Node


@Node.register_as_subclass('pull-branch-with-releases')
class PullBranchWithReleasesNode(Node):

    @classmethod
    def _handle(cls, request):
        branch_to_pull = request.branch_holding_releases
        remote_slug, urls = cls.run(cls.command('pull-branch', request.repository, branch_to_pull))

        cls.run(cls.command('render', 'pulled-branch-msg',
            request.repository.directory_path,
            branch_to_pull,
            remote_slug,
            'ssh',
            urls))

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
