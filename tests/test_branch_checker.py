import pytest
from software_release.branch_checker import BranchChecker


@pytest.fixture
def mock_git_repo():

    class MockRepo:
        def __init__(self, *args, **kwargs):
            self.active_branch = type('BranchWithName', (),
            {'name': kwargs.get('active_branch', 'master')})

        def remote(self):
            return type('MockRemote', (), {
                'url': 'git@github.com:boromir674/software-patterns.git'})
    return MockRepo


def test_branch_checker_with_mocked_repo(mock_git_repo, get_object):

    repository_factory = get_object(
        'RepositoryFactory',
        'software_release.repository_factory',
        overrides={'Repo': lambda: mock_git_repo})
    branch_checker = BranchChecker()
    repository = repository_factory.create('/data/repos/software-patterns')
    active_branch = branch_checker.active_branch(repository)
    assert active_branch.name == 'master'
