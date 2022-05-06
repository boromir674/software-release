import attr

from .repository_interface import RepositoryInterface
from .head_interface import HeadInterface


@attr.s
class Repository(RepositoryInterface):
    active_branch: HeadInterface = attr.ib()
    directory_path: str = attr.ib()
    repo_proxy = attr.ib()
