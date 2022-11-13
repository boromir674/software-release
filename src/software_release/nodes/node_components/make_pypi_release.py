from software_release.nodes.node import Node


@Node.register_as_subclass('publish-in-pypi')
class MakePypiRelease(Node):

    @classmethod
    def _handle(cls, request):
        cls.run(cls.command('render', f"Please upload distribution to pypi.",
            f" Eg use 'PACKAGE_DIST_VERSION={request.new_version} PYPI_SERVER tox -e deploy",
        ))

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
