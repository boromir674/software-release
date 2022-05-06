from software_release.nodes.node import Node


@Node.register_as_subclass('wait-for-pr-approval')
class WaitPullRequestApproval(Node):

    @classmethod
    def _handle(cls, request):

        found = cls.run(cls.command('wait-for-pr-approval', 
            "boromir674", # owner
            "software-patterns", # repo_name
            request.pull_request.number
        ))
        if found:
            print('FOUND')


    def handle(self, request):
        self._handle(request)
        return super().handle(request)
