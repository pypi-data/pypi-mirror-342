import attr

from imbue_core.local_sync import LocalSyncMessage


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class LocalSaveMessage(LocalSyncMessage):
    """Message from the local file watcher to send to client."""
