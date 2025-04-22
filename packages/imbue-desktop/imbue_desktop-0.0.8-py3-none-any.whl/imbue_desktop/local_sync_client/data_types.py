from typing import Union

import attr

from imbue_core.repo_state import CleanRepoOperation
from imbue_core.repo_state import ConflictedRepoOperation

ClientID = str


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class LocalSyncClientSettings:
    # the max time between messages for them to be considered a single message
    # NOTE: this value may need tuning
    message_buffer_time: float = 0.4
    # polling interval for the client to check for new messages from the server
    # NOTE: this value may need tuning
    server_poll_interval: float = 0.5


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class LocalRepoState:
    branch_name: str
    commit_hash: str
    repo_operation: Union[CleanRepoOperation, ConflictedRepoOperation]

    @property
    def is_conflicted(self) -> bool:
        return isinstance(self.repo_operation, ConflictedRepoOperation)


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class VersionedLocalRepoState(LocalRepoState):
    # the version of the remote repo state comes from
    version: int

    def as_unversioned_state(self) -> LocalRepoState:
        return LocalRepoState(
            branch_name=self.branch_name,
            repo_operation=self.repo_operation,
            commit_hash=self.commit_hash,
        )
