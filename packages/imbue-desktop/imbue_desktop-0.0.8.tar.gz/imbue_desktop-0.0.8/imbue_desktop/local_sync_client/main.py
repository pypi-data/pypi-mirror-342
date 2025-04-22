from imbue_core import async_monkey_patches
from imbue_core.common import is_testing
from imbue_desktop.error_utils import get_username_for_sentry
from imbue_desktop.error_utils import setup_sentry

async_monkey_patches.apply()

import asyncio
import signal
import sys
from pathlib import Path
from typing import Any
from typing import Optional

import typer
from loguru import logger
from typing_extensions import Annotated

from imbue_core.async_monkey_patches import safe_cancel
from imbue_core.async_utils import wrapped_asyncio_run
from imbue_desktop.local_sync_client.core import LocalSyncClient
from imbue_desktop.local_sync_client.utils import validate_branch_at_launch
from imbue_desktop.utils import get_api_key_from_imbue_toml
from imbue_desktop.utils import get_url_from_imbue_toml

_MAIN_LOOP: Any = None
_SYNC_CLIENT: Any = None


def _signal_handler(_signal, _frame) -> None:
    logger.debug(f"Signal handler called with signal: {_signal}. Setting IS_SHUTTING_DOWN_FROM_SIGNAL to True")
    global _IS_SHUTTING_DOWN_FROM_SIGNAL, _MAIN_LOOP
    _IS_SHUTTING_DOWN_FROM_SIGNAL = True
    asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(shutdown(), _MAIN_LOOP)


async def shutdown() -> None:
    logger.info("Shutdown called - cancelling local sync client run task")
    safe_cancel(_SYNC_CLIENT.run_task)


async def local_sync_client_loop(local_sync_repo_path: Path, server_url: str, api_key: str) -> None:
    global _IS_SHUTTING_DOWN_FROM_SIGNAL, _SYNC_CLIENT, _MAIN_LOOP
    _MAIN_LOOP = asyncio.get_running_loop()
    logger.info("Starting local sync client loop")
    _SYNC_CLIENT = LocalSyncClient(
        local_sync_repo_path=local_sync_repo_path,
        server_url=server_url,
        api_key=api_key,
    )

    signal.signal(signal.SIGINT, _signal_handler)

    _SYNC_CLIENT.set_run_task()

    assert _SYNC_CLIENT.run_task is not None
    try:
        await _SYNC_CLIENT.run_task
    except asyncio.CancelledError:
        logger.info("Sync task canceled")
    except BaseException as e:
        if _IS_SHUTTING_DOWN_FROM_SIGNAL:
            logger.info(f"Sync task canceled: {e}")
        else:
            logger.debug("Sync task failed")
            raise e
    finally:
        logger.info("local sync client loop closing")
        await _SYNC_CLIENT.close()
        logger.info("local sync client loop closed")

    logger.info("CRAFTY_SHUTDOWN_CLEANLY")
    if _IS_SHUTTING_DOWN_FROM_SIGNAL:
        sys.exit(130)


def _main(
    local_sync_repo_path: Path,
    server_url: Annotated[Optional[str], typer.Argument()] = None,
    api_key: Optional[str] = None,
    branch_name: Optional[str] = None,
    reset_to_remote: bool = False,
) -> None:
    global _IS_SHUTTING_DOWN_FROM_SIGNAL

    if server_url is None:
        server_url = get_url_from_imbue_toml()
    # We don't try to get the server URL from foreman when manually running local sync.
    assert server_url is not None, "Server URL must be provided"

    if api_key is None:
        api_key = get_api_key_from_imbue_toml()

    if not is_testing():
        sentry_username = get_username_for_sentry(api_key=api_key)
        setup_sentry(username=sentry_username)

    validate_branch_at_launch(local_sync_repo_path, branch_name, reset_to_remote)

    wrapped_asyncio_run(
        local_sync_client_loop(
            local_sync_repo_path=local_sync_repo_path,
            server_url=server_url,
            api_key=api_key,
        )
    )

    if _IS_SHUTTING_DOWN_FROM_SIGNAL:
        sys.exit(130)
    else:
        sys.exit(0)


_IS_SHUTTING_DOWN_FROM_SIGNAL = False


# Another level of nesting to make this work as a "pyproject script".
def main() -> None:
    app = typer.Typer(pretty_exceptions_enable=False)
    app.command()(_main)
    app()


if __name__ == "__main__":
    typer.run(main)
