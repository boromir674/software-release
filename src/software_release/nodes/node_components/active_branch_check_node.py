from software_release.nodes.node import Node
import sys


@Node.register_as_subclass('active-branch-check')
class ActiveBranchCheckNode(Node):

    @classmethod
    def _handle(cls, request):
        cmd = cls.command('check-branches', request.repository)
        is_release_branch = cls.run(cmd)
        
        return is_release_branch

    def handle(self, request):
        is_release_branch = self._handle(request)
        if is_release_branch:
            cmd = type(self).command('render', 'release-branch-msg', request.repository.active_branch.name)
            type(self).run(cmd)
            request.branch_holding_releases = 'master'  # todo make it a runtime argument
            return super().handle(request)
        else:
            cmd = type(self).command('render', 'no-release-branch-msg', request.repository.active_branch.name)
            type(self).run(cmd)
            cmd = type(self).command('render',
                'Please navigate to the local repository, checkout a \'release\' branch and rerun the wizard')
            type(self).run(cmd)
            sys.exit(1)
