class SwitchError(Exception):
    def __init__(self, unmatched_case: object) -> None:
        super().__init__(f"Failed to match: {unmatched_case}")


class NoAPIKeyError(Exception):
    def __init__(self) -> None:
        super().__init__("No API key provided and no API key found in ~/.imbue.toml")


class NoURLError(Exception):
    def __init__(self) -> None:
        super().__init__("No URL provided and no URL found in ~/.imbue.toml")


class LocalSyncClientError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class SaveResultError(LocalSyncClientError):
    pass


class StreamCloseError(LocalSyncClientError):
    pass


class ActiveBranchUnknownError(LocalSyncClientError):
    pass
