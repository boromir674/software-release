from .abstract_commit_generator import AbstractCommitGenerator
from software_release.commit_interface import CommitFactory


class BranchCommitsGenerator(AbstractCommitGenerator):
    """Instaces are generators yielding the whole commit history of a branch."""
    
    def generate_commits(self, repository, revision):
        for git_commit in repository.repo_proxy.iter_commits(str(revision)):
            yield CommitFactory.from_git_commit(git_commit)

