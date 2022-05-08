from software_release.push_active_branch_interface import PushActiveBranchInterface


class ActiveBranchPusher(PushActiveBranchInterface):

    def push(self, repository, remote_server_slug='origin'):
        # TODO: use the git API to implement t he push method
        # https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131
        origin = repository.repo_proxy.remote(name=remote_server_slug)
        origin.push()
        self.remote_slug = remote_server_slug
        self.urls = [_ for _ in origin.urls]
