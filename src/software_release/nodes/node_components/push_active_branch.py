from typing import List
from software_release.nodes.node import Node


@Node.register_as_subclass('push-active-branch')
class PushActiveBranchNode(Node):

    @classmethod
    def _handle(cls, request):

        command = cls.command('push-active-branch', request.repository)
        remote_server_name_slug: str
        remote_urls: List[str]

        remote_server_name_slug, remote_urls = cls.run(command)

        command = cls.command('render', 'pushed-active-branch',
            request.repository.directory_path,
            request.repository.active_branch.name,
            remote_server_name_slug,
            'ssh',
            remote_urls
        )
        cls.run(command)
    
    def handle(self, request):
        self._handle(request)
        return super().handle(request)
