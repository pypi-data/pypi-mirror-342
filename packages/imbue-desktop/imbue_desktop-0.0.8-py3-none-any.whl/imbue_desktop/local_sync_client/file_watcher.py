import asyncio
import subprocess
import time
from contextlib import asynccontextmanager
from pathlib import Path
from queue import Queue
from typing import AsyncGenerator
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Self

import anyio
from loguru import logger
from watchdog.events import EVENT_TYPE_DELETED
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from imbue_core.async_monkey_patches import log_exception
from imbue_core.local_sync import get_current_time
from imbue_desktop.local_sync_client.message_types import LocalSaveMessage


class LocalSyncClientFileWatcher(FileSystemEventHandler):
    """A file watcher that is used to watch the local client for changes.

    This is just the AutosyncFileWatcher but handles sending events to the local client service.
    """

    _file_watcher_lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, directory_to_watch: Path, message_queue: Queue[LocalSaveMessage]) -> None:
        logger.debug(f"LocalSyncClientFileWatcher __init__ {directory_to_watch}")
        self.directory_to_watch = directory_to_watch
        self.is_running: bool = True
        self.last_modification_event_time_by_path: Dict[str, float] = {}
        self.last_direct_modification_time_by_path: Dict[str, float] = {}
        self._callback: Optional[Callable[[str, Optional[str]], None]] = None

        # queue for add events too
        self.message_queue = message_queue

        try:
            self._observer = Observer()
            self._observer.schedule(self, path=str(self.directory_to_watch.resolve()), recursive=True)
            self._observer.start()
        except RuntimeError as e:
            if "it is already scheduled" in str(e):
                logger.trace("File watcher is already scheduled, ignoring")
            else:
                raise

    def on_modified(self, event: FileSystemEvent) -> None:
        if self._record_and_check_ignore(event, self.directory_to_watch):
            return
        # only log if the file is not ignored, to avoid spamming the logs
        logger.trace(f"Detected changes in the following file: {event.src_path}")

        # so dumb that pycharm doesn't save atomically
        # something related could be enabled: https://www.jetbrains.com/help/pycharm/system-settings.html
        # but then we will have to do a race-y check for whether that backup exists
        # so instead, we just wait a bit here for the save to finish...
        sleep_until = time.monotonic() + 0.1
        time_to_sleep = sleep_until - time.monotonic()
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

        self._handle_file_event(event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if self._record_and_check_ignore(event, self.directory_to_watch):
            return
        logger.trace(f"Detected removal of the following file: {event.src_path}")
        self._handle_file_event(event)

    def on_created(self, event: FileSystemEvent) -> None:
        if self._record_and_check_ignore(event, self.directory_to_watch):
            return
        logger.trace(f"Detected creation of the following file: {event.src_path}")
        self._handle_file_event(event)

    def _handle_file_event(self, event: FileSystemEvent) -> None:
        if not self.is_running:
            logger.trace(f"File watcher is not running, ignoring file event: {event}")
            return
        logger.trace(f"Handling file event: {event}")
        self._maybe_call_callback(event)
        # Josh note -- eh, idk about that.  If you create an empty file, I'm not sure if it will be modified
        # if event.event_type != EVENT_TYPE_CREATED:
        #     # don't save creation events, as these are always followed by a modification event, which
        #     # is what we will send
        #     message = LocalSaveMessage(created_at=get_current_time())
        #     self.message_queue.put_nowait(message)
        #     logger.trace(f"Message added to queue: {message} {self.directory_to_watch}")
        # Josh: so I just changed it to this:
        message = LocalSaveMessage(created_at=get_current_time())
        self.message_queue.put_nowait(message)
        logger.trace(f"Message added to queue: {message} {self.directory_to_watch}")

    def _record_and_check_ignore(self, event: FileSystemEvent, directory_to_watch: Path) -> bool:
        src_path = event.src_path
        if isinstance(event.src_path, bytes):
            src_path = event.src_path.decode("utf-8")
        else:
            src_path = str(event.src_path)

        self.last_modification_event_time_by_path[src_path] = time.monotonic()
        if not self.is_running:
            return True
        # NOTE: need to use `.resolve()` here because watchdog events use resolved paths
        # i.e. where any symlinks are expanded. This is compared to `.absolute()` which does not expand symlinks.
        # This is a particular issue when using `/tmp` on OSX, which is a symlink to `/private/tmp`.
        dir_to_watch_str = str(directory_to_watch.resolve())
        is_file_in_dir = src_path.startswith(dir_to_watch_str)
        if not is_file_in_dir:
            return True
        is_delete = event.event_type == EVENT_TYPE_DELETED
        if self._is_ignoring_file(Path(src_path), is_delete):
            return True
        return False

    def _maybe_call_callback(self, event: FileSystemEvent) -> None:
        if self._callback is None:
            return
        if isinstance(event.src_path, bytes):
            src_path = event.src_path.decode("utf-8")
        else:
            src_path = str(event.src_path)

        # if not src_path.endswith(TEMP_FILE_NAME):
        logger.trace(f"Calling callback for event {event.event_type} for file {src_path}")
        contents = None if event.event_type == EVENT_TYPE_DELETED else Path(src_path).read_text()
        self._callback(src_path, contents)

    async def write_file(self, relative_path: anyio.Path, file_contents: Optional[str]) -> None:
        full_path = anyio.Path(self.directory_to_watch) / anyio.Path(relative_path)
        self.last_direct_modification_time_by_path[str(full_path)] = time.time()
        if file_contents is None:
            await full_path.unlink(missing_ok=True)
        else:
            try:
                await full_path.write_text(file_contents)
            except FileNotFoundError:
                await full_path.parent.mkdir(parents=True, exist_ok=True)
                await full_path.write_text(file_contents)

    def suspend(self) -> None:
        assert self.is_running, "Cannot suspend a file watcher that is already suspended"
        self.is_running = False
        self.last_direct_modification_time_by_path.clear()

    def resume_without_wait(self) -> None:
        self.is_running = True

    def resume(self, wait_seconds: float = 10.0, slush_time: float = 0.5) -> None:
        """slush_time is to ensure that file watchers have a chance to run."""
        # wait until we've gotten events for all files we've written since we started being suspended
        start_time = time.monotonic()
        while time.monotonic() - start_time < wait_seconds:
            is_modification_complete_for_all_files = True
            for path, direct_modification_time in self.last_direct_modification_time_by_path.items():
                modified_time = self.last_modification_event_time_by_path.get(path, None)
                if modified_time is None:
                    is_modification_complete_for_all_files = False
                    break
                if modified_time < direct_modification_time:
                    is_modification_complete_for_all_files = False
                    break
                if time.monotonic() - modified_time < slush_time:
                    is_modification_complete_for_all_files = False
                    break
            if is_modification_complete_for_all_files:
                self.is_running = True
                return
            time.sleep(0.1)
        missing_files = [str(path) for path in self.last_direct_modification_time_by_path.keys()]
        raise Exception(
            f"Failed to resume file watcher after {wait_seconds} seconds!  Waiting for event from these files: {missing_files}"
        )

    @asynccontextmanager
    async def disable(self) -> AsyncGenerator[Self, None]:
        async with self._file_watcher_lock:
            self.suspend()
            try:
                yield self
                # call resume from a thread
                await anyio.to_thread.run_sync(self.resume)
                logger.debug("Enabled file watcher normally")
            except asyncio.CancelledError:
                self.resume_without_wait()
                logger.debug("Enabled file watcher (bc of cancelation)")
                raise
            except BaseException as e:
                log_exception(e, "Crazy error in file watcher")
                self.resume_without_wait()
                logger.debug("Enabled file watcher (bc of error)")
                raise
            finally:
                logger.debug("File watcher context exited")

    def add_observer(self, callback: Callable[[str, Optional[str]], None]) -> None:
        self._callback = callback

    def clear_observer(self) -> None:
        self._callback = None

    @asynccontextmanager
    async def observe_file_changes(self, callback: Callable[[str, Optional[str]], None]) -> AsyncGenerator[Self, None]:
        async with self._file_watcher_lock:
            logger.debug("Adding observer to file watcher")
            self.add_observer(callback)
            try:
                yield self
                # call resume from a thread
                await anyio.to_thread.run_sync(self.resume)
            finally:
                logger.debug("Removing observer from file watcher")
                self.clear_observer()

    def close(self) -> None:
        logger.debug("Closing file watcher")
        self._observer.stop()
        logger.debug("File watcher closed")

    def _is_ignoring_file(self, file_path: Path, is_delete: bool = False) -> bool:
        if not is_delete and not file_path.exists():
            # logger.trace(f"Ignoring file {file_path} because it does not exist and was not just deleted.")
            return True
        if file_path.is_dir():
            # logger.trace(f"Ignoring file {file_path} because it is a directory.")
            return True
        if "/.git/" in str(file_path):
            if file_path.name in ["HEAD", "COMMIT_EDITMSG"] or "/refs/heads/" in str(file_path):
                # logger.debug(
                #     f"Not ignore file {file_path} because detected potential commit-related file change: {file_path}",
                # )
                return False
            # logger.trace(f"Ignoring file {file_path} because it is in .git directory.")
            return True
        if "/.vite/" in str(file_path):
            # logger.trace(f"Ignoring file {file_path} because it is a vite directory.")
            return True
        if "/.mypy_cache/" in str(file_path):
            # logger.trace(f"Ignoring file {file_path} because it is a mypy cache directory.")
            return True
        if file_path.name == "generated-routes.ts":
            # logger.trace(f"Ignoring file {file_path} because it is a generated routes file.")
            return True
        if file_path.name == "generated-types.ts":
            # logger.trace(f"Ignoring file {file_path} because it is a generated types file.")
            return True
        if file_path.suffix == ".working":
            # logger.trace(f"Ignoring file {file_path} because it is a working file.")
            return True
        if not file_path.parent.exists():
            # logger.trace(f"Ignoring file {file_path} because its parent directory does not exist.")
            return True
        # ignore files that are gitignored by calling git check-ignore
        try:
            exit_code = subprocess.run(
                f"git check-ignore {file_path}", shell=True, check=False, capture_output=True, cwd=file_path.parent
            ).returncode
        except FileNotFoundError:
            # if the parent dir was deleted, it'll throw this error
            # logger.trace(f"Ignoring file {file_path} because its parent directory does not exist.")
            return True
        if exit_code == 0:
            # logger.trace(f"Ignoring file {file_path} because it is gitignored.")
            return True
        # logger.trace(f"Not ignoring file {file_path}.")
        return False
