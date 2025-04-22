from imbue_core import async_monkey_patches  # isort: skip

async_monkey_patches.apply()  # isort: skip

import atexit
import signal
import subprocess
import sys
import urllib.parse
from typing import Annotated
from typing import Any
from typing import Optional

import typer

from imbue_core.async_utils import wrapped_asyncio_run
from imbue_core.common import is_testing
from imbue_desktop.error_utils import get_username_for_sentry
from imbue_desktop.error_utils import setup_sentry
from imbue_desktop.errors import NoURLError
from imbue_desktop.foreman import DEFAULT_FOREMAN_URL
from imbue_desktop.foreman import get_or_create_sculptor_server
from imbue_desktop.qt import ImbueApplication
from imbue_desktop.utils import get_api_key_from_imbue_toml
from imbue_desktop.utils import get_url_from_imbue_toml

_APP: Any = None


def _main(
    sync_local_repo_path: str,
    server_url: Annotated[Optional[str], typer.Argument()] = None,
    api_key: Optional[str] = None,
    foreman_url: Optional[str] = None,
    foreman_force_new_instance: bool = False,
) -> None:
    global _APP, _IS_SHUTTING_DOWN_FROM_SIGNAL

    if api_key is None:
        api_key = get_api_key_from_imbue_toml()

    if not is_testing():
        sentry_username = get_username_for_sentry(api_key=api_key)
        setup_sentry(username=sentry_username)

    if server_url is None:
        server_url = get_url_from_imbue_toml(is_error_raised_if_not_present=False)
    if server_url is None:
        foreman_url = foreman_url or DEFAULT_FOREMAN_URL
        server_url = wrapped_asyncio_run(
            get_or_create_sculptor_server(
                api_key=api_key, foreman_url=foreman_url, is_new_instance_forced=foreman_force_new_instance
            )
        )
    if server_url is None:
        raise NoURLError()

    # Trim the path. E.g. "https://foo.modal.host/dev" -> "https://foo.modal.host".
    parsed = urllib.parse.urlparse(server_url)
    server_url_trimmed = parsed.scheme + "://" + parsed.netloc

    local_sync_process = subprocess.Popen(
        ["uv", "run", "imbue-local-sync", sync_local_repo_path, server_url_trimmed, "--api-key", api_key]
    )
    atexit.register(local_sync_process.terminate)

    _APP = ImbueApplication(sys.argv, server_url=server_url, api_key=api_key)
    _APP.register_signal_handler(signal.SIGINT, _signal_handler)
    result = _APP.exec()
    if _IS_SHUTTING_DOWN_FROM_SIGNAL:
        sys.exit(130)
    else:
        sys.exit(result)


_IS_SHUTTING_DOWN_FROM_SIGNAL = False


def _signal_handler(_signal, _frame) -> None:
    global _IS_SHUTTING_DOWN_FROM_SIGNAL, _APP
    _IS_SHUTTING_DOWN_FROM_SIGNAL = True
    _APP.quit()


# Another level of nesting to make this work as a "pyproject script".
def main() -> None:
    typer.run(_main)


if __name__ == "__main__":
    main()
