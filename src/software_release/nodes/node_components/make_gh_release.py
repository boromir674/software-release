from software_release.nodes.node import Node


@Node.register_as_subclass('make-gh-release')
class MakeGithubRelease(Node):

    @classmethod
    def _handle(cls, request):
        cls.run(cls.command('render', f"Please create a new Github release.",
            f" Eg use 'gh release create v{request.new_version}'",
        ))

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
