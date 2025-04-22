import asyncio
import hashlib
import json
import os.path
import socket
import time
from contextlib import asynccontextmanager
from pathlib import Path
from queue import Empty
from queue import Queue
from typing import AsyncGenerator
from typing import List
from typing import Optional
from typing import Tuple

import aiohttp
import anyio
from aiohttp import ClientConnectorError
from aiohttp import ClientResponseError
from aiohttp import ServerDisconnectedError
from aiohttp import ServerTimeoutError
from loguru import logger
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import wait_random_exponential

from imbue_core.async_monkey_patches import safe_cancel_and_wait_for_cleanup
from imbue_core.cattrs_serialization import deserialize_from_dict
from imbue_core.cattrs_serialization import deserialize_from_json
from imbue_core.cattrs_serialization import serialize_to_dict
from imbue_core.clean_tasks import create_clean_task
from imbue_core.computing_environment.computing_environment import apply_patch_via_git_with_conflict_markers
from imbue_core.computing_environment.computing_environment import get_branch_name
from imbue_core.computing_environment.computing_environment import get_modified_file_contents_by_path
from imbue_core.computing_environment.computing_environment import get_most_recent_sibling_branch_of_branch
from imbue_core.computing_environment.computing_environment import get_staged_unstaged_and_combined_diffs
from imbue_core.computing_environment.computing_environment import get_unmerged_and_staged_blob_contents_by_hash
from imbue_core.computing_environment.computing_environment import is_detached_head
from imbue_core.computing_environment.computing_environment import write_blob_content_by_hash
from imbue_core.computing_environment.data_types import RunCommandError
from imbue_core.frozen_utils import FrozenDict
from imbue_core.git import LocalGitRepo
from imbue_core.local_sync import AppliedSaveMessage
from imbue_core.local_sync import CreateProjectMessage
from imbue_core.local_sync import FailedToSaveMessage
from imbue_core.local_sync import GetProjectMessage
from imbue_core.local_sync import LocalSyncClientInfo
from imbue_core.local_sync import LocalSyncClientMessage
from imbue_core.local_sync import LocalSyncMessage
from imbue_core.local_sync import LocalSyncServerMessage
from imbue_core.local_sync import NewLocalRepoStateMessage
from imbue_core.local_sync import NewProjectMessage
from imbue_core.local_sync import NewRemoteRepoStateMessage
from imbue_core.local_sync import Project
from imbue_core.local_sync import SyncBranchMessage
from imbue_core.local_sync import SyncedMessage
from imbue_core.repo_state import ConflictedRepoOperation
from imbue_core.repo_state_utils import get_conflict_type_from_computing_environment
from imbue_core.repo_state_utils import get_special_git_file_contents_by_path_for_conflict_type
from imbue_core.retry_utils import log_before_sleep
from imbue_desktop.errors import ActiveBranchUnknownError
from imbue_desktop.errors import SaveResultError
from imbue_desktop.errors import StreamCloseError
from imbue_desktop.local_sync_client.data_types import CleanRepoOperation
from imbue_desktop.local_sync_client.data_types import ClientID
from imbue_desktop.local_sync_client.data_types import LocalRepoState
from imbue_desktop.local_sync_client.data_types import LocalSyncClientSettings
from imbue_desktop.local_sync_client.data_types import VersionedLocalRepoState
from imbue_desktop.local_sync_client.file_watcher import LocalSyncClientFileWatcher
from imbue_desktop.local_sync_client.utils import add_project_to_lock_file
from imbue_desktop.local_sync_client.utils import get_project_name_from_local_repo
from imbue_desktop.local_sync_client.utils import is_client_already_running
from imbue_desktop.local_sync_client.utils import is_local_repo_states_equal
from imbue_desktop.local_sync_client.utils import remove_project_from_lock_file
from imbue_desktop.utils import get_or_create_machine_id

# how frequently to check that yes, in fact, our state is still valid
_SANITY_POLL_TIME = 10.0


retry_logic = retry(
    # max 5 seconds wait time because this is your own server, so do whatever you want to it!
    wait=wait_random_exponential(multiplier=0.25, max=5, exp_base=2),
    reraise=True,
    retry=retry_if_exception_type((ClientConnectorError, ServerDisconnectedError, ServerTimeoutError)),
    before_sleep=log_before_sleep,
)


def get_client_info() -> LocalSyncClientInfo:
    """Get the client info for the current machine."""
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except Exception:
        logger.error("Failed to get ip address for client info")
        ip_address = "unknown"
    return LocalSyncClientInfo(ip_address=ip_address)


def _fix_api_key(api_key: str, project: Project) -> Project:
    git_url = project.backend_repo_url
    # Add the api key as a username/password to the git URL.
    if api_key:
        git_url = git_url.replace("://", f"://api:{api_key}@")
    return Project(name=project.name, id=project.id, backend_repo_url=git_url)


class ServerMessageStream:
    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.response = response
        self.content_iterator = aiter(response.content)

    async def __aiter__(self) -> AsyncGenerator[LocalSyncServerMessage, None]:
        async for line in self.content_iterator:
            data = line.decode("utf-8").split(": ", maxsplit=1)[-1].strip()
            if data == "null":
                raise StreamCloseError("Not expecting this stream to close...")
            # FIXME: maybe we could stop doing this though, it's strange...
            # idk why but we send data with two \n's, so, whatever, have to ignore it here
            if data != "":
                yield deserialize_from_json(data)

    async def __anext__(self) -> LocalSyncServerMessage:
        return await self.__aiter__().__anext__()


class LocalSyncClient:
    """
    The local client service for syncing local and remote repo states.

    Local Sync Client Service that uses HTTP requests to communicate with the server.

    This implementation works with a remote server via HTTP communication, allowing
    the client and server to be on different machines.
    """

    def __init__(
        self,
        local_sync_repo_path: Path,
        server_url: str,
        api_key: str,
        settings: Optional[LocalSyncClientSettings] = None,
    ) -> None:
        super().__init__()
        # the path to the local sync repo
        self.local_sync_repo_path = local_sync_repo_path
        # the settings for the local sync client
        self.settings = settings or LocalSyncClientSettings()
        # the name of the project
        self._project_name = None
        # the actual file watcher class
        self._file_watcher = None
        # Queue for getting messages from the file watcher
        # NOTE: this cannot be an asyncio.Queue because the file watcher runs on a different thread
        self._file_watcher_message_queue = Queue()
        # task for reading messages from the file watcher queue and adding them to the message queue
        self._file_watcher_message_reader_task = None
        # this gets flipped whenever we notice that some files were changed (after accounting for debouncing)
        self.want_to_save_flag = asyncio.Event()
        # the async task for the agent's .run method, this is added by the start_agent function
        self.run_task = None
        # the current user message that is being processed
        self.current_message = None
        # list of user messages that have been received and processed
        self.messages: Tuple[LocalSyncMessage, ...] = tuple()
        # most recently received remote repo state
        self._last_remote_repo_state: Optional[VersionedLocalRepoState] = None
        self._local_repo_lock = asyncio.Lock()
        self._is_done = False
        # The base URL of the server we're communicating with
        self.server_url = server_url
        # our API key, for authentication
        self.api_key = api_key

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[aiohttp.ClientSession, None]:
        """Get the HTTP session for the client."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(
                total=None,
                connect=30,
                sock_connect=30,
                sock_read=None,
            ),
        )
        try:
            yield session
        finally:
            await session.close()

    @asynccontextmanager
    async def _make_get_request(self, endpoint: str) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        async with self._get_session() as session:
            async with session.get(endpoint) as response:
                yield response

    @asynccontextmanager
    async def _make_post_request(self, endpoint: str, json: dict) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        async with self._get_session() as session:
            async with session.post(endpoint, json=json) as response:
                yield response

    @retry_logic
    async def _send_message(self, message: LocalSyncClientMessage) -> LocalSyncServerMessage:
        """Async implementation of sending a user event to the backend."""
        message_json = serialize_to_dict(message)
        async with self._make_post_request(
            f"{self.server_url}/api/local_sync/process_message", json=message_json
        ) as response:
            response.raise_for_status()
            response_json = await response.json()
            logger.debug("Received message response on local sync client")
            return deserialize_from_dict(response_json)

    @retry_logic
    async def _get_project_from_backend(self) -> Optional[Project]:
        logger.debug("Getting project from the server")
        request_url = f"{self.server_url}/api/local_sync/project/{await self.get_project_name()}"
        async with self._make_get_request(request_url) as response:
            response.raise_for_status()
            message = deserialize_from_dict(await response.json())
            assert isinstance(message, GetProjectMessage)
            if message.project is None:
                return None
            return _fix_api_key(self.api_key, message.project)

    def get_previous_client_branch_file_path(self) -> anyio.Path:
        return anyio.Path(os.path.expanduser(f"~/.imbue/selected_branch_cache/{self.client_id}"))

    # sigh.  We need to save a bit of extra state so that we can start up from detached head states
    async def _load_previous_branch_name(self, repo: LocalGitRepo) -> Optional[str]:
        state_file = self.get_previous_client_branch_file_path()
        if await state_file.exists():
            previous_commit_hash, previous_branch = (await state_file.read_text()).strip().split("|", maxsplit=1)
            current_commit_hash = await repo.head_hash()
            is_in_detached_head = await is_detached_head(repo)
            if not is_in_detached_head:
                return previous_branch
            # we should ensure that we are ALSO still at the same commit hash, if not, this should return None
            if current_commit_hash == previous_commit_hash:
                return previous_branch
        return None

    async def _save_previous_branch_name(self, repo_state: VersionedLocalRepoState) -> None:
        state_file = self.get_previous_client_branch_file_path()
        await state_file.parent.mkdir(parents=True, exist_ok=True)
        await state_file.write_text(f"{repo_state.commit_hash}|{repo_state.branch_name}")

    @retry_logic
    async def _create_project_on_backend(self) -> Project:
        logger.debug("Creating project on the server")
        request_url = f"{self.server_url}/api/local_sync/create_project"
        message = CreateProjectMessage(
            project_name=await self.get_project_name(), client_id=self.client_id, client_info=get_client_info()
        )
        message_json = serialize_to_dict(message)
        async with self._make_post_request(request_url, json=message_json) as response:
            response.raise_for_status()
            message = deserialize_from_dict(await response.json())
            assert isinstance(message, GetProjectMessage)
            assert message.project is not None
            project = _fix_api_key(self.api_key, message.project)
            assert (
                project.name == message.project.name
            ), f"Unexpected project name: {project.name} != {message.project.name}"
            return project

    @retry_logic
    async def _sync_branch(
        self, starting_state: LocalRepoState, project: Project, user_choice: Optional[str] = None
    ) -> str:
        logger.debug(
            f"Syncing our branch with the server: {starting_state.branch_name} from {self.local_sync_repo_path=}"
        )
        # figure out which branch we're starting from
        target_branch_name = await _get_target_branch_name(
            starting_state, self._last_remote_repo_state, self.local_sync_repo_path
        )
        logger.debug(f"Target branch is {target_branch_name}")

        # FIXME: someday perhaps we can be a little bit smarter about whether we have pushed or not
        #  but for now, just be safe and make sure it is available remotely
        await self._push_new_commit_to_backend(
            starting_state.commit_hash, starting_state.branch_name, project, target_branch_name=target_branch_name
        )

        # then call the sync method
        request_url = f"{self.server_url}/api/local_sync/sync_branch"
        message = SyncBranchMessage(
            client_id=self.client_id,
            project_id=project.id,
            client_info=get_client_info(),
            branch_name=starting_state.branch_name,
            target_branch_name=target_branch_name,
            commit_hash=starting_state.commit_hash,
            repo_operation=starting_state.repo_operation,
            user_choice=user_choice,
        )
        message_json = serialize_to_dict(message)
        logger.debug("Sending branch sync message")
        async with self._make_post_request(request_url, json=message_json) as response:
            response.raise_for_status()
            result = json.loads((await response.content.read()).decode("utf-8"))
            return result

    @property
    def client_id(self) -> ClientID:
        # client id is a hash of the machine id and the local repo path, so that two clients started from the same local repo
        # path on different machines will have different IDs, but starting the client with the same local repo path on the same machine
        # will have the same client id
        # Importantly, we enforce upon startup that two clients don't run on the same machine with the same local repo path
        project_path_str = self.local_sync_repo_path.as_posix()
        machine_id = get_or_create_machine_id()
        client_id = f"{machine_id}-{project_path_str}-"
        # We only take 16 characters for ergonomic reasons.
        return hashlib.sha256(client_id.encode()).hexdigest()[:16]

    async def get_project_name(self) -> str:
        if self._project_name is None:
            self._project_name = await get_project_name_from_local_repo(self.local_sync_repo_path)
        return self._project_name

    def get_file_watcher(self) -> LocalSyncClientFileWatcher:
        if self._file_watcher is None:
            raise RuntimeError("File watcher not started")
        return self._file_watcher

    def set_run_task(self) -> None:
        self.run_task = create_clean_task(self.run(), is_within_new_group=True, name=f"{self.__class__.__name__}:run")

    async def _file_watcher_message_watcher(self) -> None:
        logger.debug(f"Starting file watcher message watcher for {self.local_sync_repo_path=}")
        while True:
            try:
                _message = self._file_watcher_message_queue.get_nowait()
            except Empty:
                await asyncio.sleep(0.1)
                continue
            else:
                logger.trace(f"Got message from file watcher:{self.local_sync_repo_path=}")
                # nice, something changed!  Keep getting messages until the queue is empty, or we've waited long enough
                # (basically just debouncing these)
                last_event_time = time.monotonic()
                while time.monotonic() - last_event_time < self.settings.message_buffer_time:
                    try:
                        _message = self._file_watcher_message_queue.get_nowait()
                    except Empty:
                        await asyncio.sleep(0.1)
                        continue
                # ok, all done waiting for the debouncing, just flip the flag
                logger.trace(f"Notifying main loop about save event: {self.local_sync_repo_path=}")
                self.want_to_save_flag.set()

    async def run(self) -> None:
        logger.info(f"Starting for project at path {self.local_sync_repo_path=}")

        logger.debug(f"Checking if another instance of the client is already running for {self.local_sync_repo_path=}")
        if is_client_already_running(self.local_sync_repo_path):
            raise RuntimeError("Another instance of the local sync client is already running")
        logger.debug(f"Adding project to lock file {self.local_sync_repo_path=}")
        add_project_to_lock_file(self.local_sync_repo_path)

        logger.debug(f"Starting file watcher {self.local_sync_repo_path=}")
        self._file_watcher = LocalSyncClientFileWatcher(
            directory_to_watch=self.local_sync_repo_path,
            message_queue=self._file_watcher_message_queue,
        )
        self._file_watcher_message_reader_task = create_clean_task(self._file_watcher_message_watcher())
        await self._outer_reconnect_loop()

    @retry(
        wait=wait_random_exponential(multiplier=0.5, max=5, exp_base=2),
        reraise=True,
        retry=retry_if_exception_type((ClientResponseError, StreamCloseError)),
        before_sleep=log_before_sleep,
    )
    async def _outer_reconnect_loop(self) -> None:
        project = await self._setup_project_with_server()
        await self._sync_project_forever(project)

    async def _setup_project_with_server(self) -> Project:
        # Handle any necessary project setup with the server, this should happen anytime the client or server disconnects
        # figure out the starting branch name, in case necessary
        # First see if the project already exists
        project = await self._get_project_from_backend()
        # if there is no project, we need to create it
        if project is None:
            project = await self._create_project_on_backend()
        return project

    @retry_logic
    async def _sync_project_forever(self, project: Project) -> None:
        logger.debug(f"Syncing project {project.name} forever.")

        # Now open the connection and start listening for events.
        endpoint = f"{self.server_url}/api/local_sync/subscribe/{project.id}/{self.client_id}"
        async with self._make_get_request(endpoint) as response:
            logger.info(f"Connected to sync for {project.name}")
            server_message_stream = ServerMessageStream(response)
            while True:
                try:
                    # figure out the starting state, for syncing with project
                    starting_state = await self._get_current_local_repo_state()
                    # this returns when the branch has become deselected
                    await self._sync_branch_while_active(starting_state, project, server_message_stream)
                    logger.debug("New branch detected locally! Restarting sync...")
                # if we're in a detached head state that we don't recognize, warn the user
                except ActiveBranchUnknownError:
                    # if the current branch shifts, just start over from the top
                    # FIXME: give a blocking warning on the front end as well -- you are in a weird state
                    logger.warning("You are in detached head state -- we cannot sync this.")
                    await asyncio.sleep(0.5)

    async def _sync_branch_while_active(
        self, starting_state: LocalRepoState, project: Project, server_message_stream: ServerMessageStream
    ) -> None:
        logger.debug("Syncing branch while active")
        # can safely clear the change flag here -- we'll sync stuff anyway right below
        self.want_to_save_flag.clear()

        # now that the project exists, ensure that the branch exists and is synced
        logger.debug("Checking if we are synced for this branch...")
        remote_state_description = await self._sync_branch(starting_state, project)
        if remote_state_description != "":
            logger.debug(f"Remote state is supposedly different:\n{remote_state_description}")
            logger.debug("Sending initial branch state in order to sync...")
            # if we get back a remote state, that's because our code is incompatible with the remote
            # that means that the user must decide what to do
            user_choice = await self._handle_conflicted_branch(starting_state, remote_state_description, project)
            # then we can sync the branch again, and this time it is guaranteed to succeed
            await self._sync_branch(starting_state, project, user_choice=user_choice)

        logger.debug("Waiting for Synced event")
        # Now discard everything until we get a Synced event
        # (that is what indicates that the server is ready to start syncing)
        # (the event will be created by our call to create_project or sync_project above)
        current_save_task: Optional[asyncio.Task[AppliedSaveMessage | FailedToSaveMessage] | None] = None
        new_file_change_event_task: asyncio.Task | None = None
        last_clean_save_version = 0
        async for message in server_message_stream:
            if isinstance(message, SyncedMessage):
                logger.debug("Synced event received")
                # set our initial "remote" state, we should be synced now!
                new_repo_state = VersionedLocalRepoState(
                    branch_name=message.branch_name,
                    version=message.version,
                    commit_hash=message.commit_hash,
                    repo_operation=message.repo_operation,
                )
                self._last_remote_repo_state = new_repo_state

                # if there is a pending save that happened during the sync process itself,
                # then we need to ask the user how they want to resolve things.
                is_conflicted = self.want_to_save_flag.is_set()
                if is_conflicted:
                    logger.debug("Pending save detected while waiting for synced event. Handling conflict.")
                    is_using_local_changes = await self._prompt_user_about_commit_conflict()
                    if is_using_local_changes:
                        current_save_task = await self._resolve_commit_conflict_using_local_changes(
                            new_repo_state, project
                        )
                        if current_save_task is not None:
                            new_file_change_event_task = asyncio.create_task(self.want_to_save_flag.wait())
                    else:
                        # FIXME: actually implement this
                        logger.debug("Decided to handle remote commit conflict by using REMOTE changes")
                        # # not too hard to implement, something like this (same code as below)
                        # message = pending_messages[-1]
                        # await self._process_new_repo_state_message(message, project)
                        # pending_messages.clear()
                        raise NotImplementedError()

                # no matter what, ready to move down to the main sync loop
                logger.debug("LOCAL_SYNC_STARTED")
                last_clean_save_version = message.version
                break
            else:
                logger.debug(f"Discarding message from server while waiting for Synced event: {message}")

        assert (
            self._last_remote_repo_state is not None
        ), "Should have received at least one state from the server at this point"

        logger.debug("Entering main sync loop")

        # And finally, now that we have found the Synced event, we process messages as they arrive.
        # There is a bit of complexity here, because of save events -- we don't want to have more than one
        # outstanding save event at once, and only once we are finished saving our local changes do we
        # actually work through certain types of server messages (eg, those that would cause us to change
        # our underlying git hash)
        new_remote_state_messages: List[NewRemoteRepoStateMessage] = []
        next_message_task = asyncio.create_task(anext(server_message_stream))
        if new_file_change_event_task is None:
            new_file_change_event_task = asyncio.create_task(self.want_to_save_flag.wait())
        periodic_sanity_check_wait_task = asyncio.create_task(asyncio.sleep(_SANITY_POLL_TIME))
        conflict_version: Optional[int] = None

        try:
            while True:
                logger.debug("# Waiting for next event")
                # we wait for 1 of 4 things:
                next_events = [
                    # a new message from the server
                    next_message_task,
                    # any pending save event to finish
                    *([current_save_task] if current_save_task else []),
                    # some file was modified locally. This includes files in the .git folder! (ie, can signal branch change)
                    *([new_file_change_event_task] if new_file_change_event_task else []),
                    # a periodic sanity check to make sure we are at the state we expect
                    periodic_sanity_check_wait_task,
                ]
                await asyncio.wait(next_events, return_when=asyncio.FIRST_COMPLETED)
                logger.debug("# Next event received")

                # handle the case that there is a new message
                if next_message_task.done():
                    logger.debug("## Next message task done. New message recieved from server, processing...")
                    next_processed_message = _process_next_message_from_server(next_message_task)
                    if next_processed_message is not None:
                        new_remote_state_messages.append(next_processed_message)
                        logger.debug(
                            f"New remote state message received from server, added to list of new messages ({len(new_remote_state_messages)} total)"
                        )
                    next_message_task = asyncio.create_task(anext(server_message_stream))

                # we finished saving
                if current_save_task is not None and current_save_task.done():
                    logger.debug("## Current save task done.")
                    # see what happened:
                    save_result = current_save_task.result()
                    # we're not saving anymore
                    current_save_task = None

                    if isinstance(save_result, FailedToSaveMessage):
                        # if we are conflicted (i.e. a local change was rejected by the server), have to deal with that immediately.
                        logger.debug("### Failed to save remotely, handling conflict.")
                        conflict_version = save_result.version
                    elif isinstance(save_result, AppliedSaveMessage):
                        logger.debug("### Remote save completed successfully")
                        if not save_result.is_containing_new_changes:
                            last_clean_save_version = save_result.version
                        else:
                            # otherwise there are new changes, so they will get applied by the next update message
                            # in a sense, this save is "unclean", bc we need some changes from the server
                            # they will appear as a remote state update anyway.
                            pass
                    else:
                        raise SaveResultError(f"Unexpected save result: {save_result}")

                if self.want_to_save_flag.is_set():
                    logger.debug("## New local changes detected.")
                    if new_file_change_event_task is not None:
                        await new_file_change_event_task
                        new_file_change_event_task = None

                    # first check whether the branch has changed locally
                    current_local_branch_name = await self._definitely_get_current_branch_name()
                    is_new_branch = (
                        current_local_branch_name is not None
                        and current_local_branch_name != starting_state.branch_name
                    )
                    if is_new_branch:
                        logger.debug(
                            f"### Local file changes appear to have involved changing to a new branch: {current_local_branch_name=} {starting_state.branch_name=}"
                        )
                        logger.debug("### Exiting sync loop for current branch.")
                        # we need to make sure that our save event resolves
                        # FIXME: we could be more careful in this case.
                        #  right now we simply wait for the event and hope that it worked
                        #  however, if it fails, we could look into the details
                        #  In the case where we stashed those changes anyway, whatever, we can move on
                        #  In the case where we committed, we may need to prompt the user about which commit to use
                        if current_save_task is not None:
                            logger.debug("Waiting for save task to finish before moving to new branch")
                            await current_save_task
                            current_save_task = None
                        return

                # handle the sanity check
                if periodic_sanity_check_wait_task.done():
                    logger.debug("## Periodic sanity check")
                    if (
                        # we're not saving
                        current_save_task is None
                        # there's no conflict
                        and conflict_version is None
                        # we don't want to save
                        and not self.want_to_save_flag.is_set()
                        # there are no new remote state messages
                        and len(new_remote_state_messages) == 0
                    ):
                        # then we should make sure that *if* we saved, we would end up at the right place
                        current_state_to_validate = await self._get_current_local_repo_state()
                        if current_state_to_validate.repo_operation != self._last_remote_repo_state.repo_operation:
                            # FIXME: add some extra error reporting here
                            logger.error(
                                f"Client seems de-synced.\n Current state: {current_state_to_validate}\n Last remote state: {self._last_remote_repo_state}"
                            )
                            # if we ever see this, we'll need to dig into why & whether you can recover by re-saving
                    periodic_sanity_check_wait_task = asyncio.create_task(asyncio.sleep(_SANITY_POLL_TIME))

                # now figure out what to do next.

                if conflict_version is not None:
                    if current_save_task is not None:
                        logger.debug("Waiting for save task to finish before resolving conflict")
                        await current_save_task
                        current_save_task = None

                    logger.debug("### Prompting user about conflict")
                    # need the user to weigh in on what to do, sorry user
                    is_using_local_changes = await self._prompt_user_about_commit_conflict()
                    if is_using_local_changes:
                        logger.debug("### User decided to use local changes")
                        # we must make sure that we've caught up to the remote state before we save
                        # so that there are no more conflicts
                        latest_message = _get_most_recent_remote_state_message(new_remote_state_messages)
                        new_remote_state_messages.clear()
                        while latest_message is None or latest_message.version < conflict_version:
                            logger.debug(
                                f"Ensuring that we have remote state version={conflict_version} before resolving conflict"
                            )
                            await next_message_task
                            latest_message = _process_next_message_from_server(next_message_task)
                            next_message_task = asyncio.create_task(anext(server_message_stream))

                        # ok, we've finally caught up, so now we can just try saving again
                        new_repo_state = VersionedLocalRepoState(
                            branch_name=latest_message.branch_name,
                            version=latest_message.version,
                            commit_hash=latest_message.commit_hash,
                            repo_operation=latest_message.repo_operation,
                        )
                        self._last_remote_repo_state = new_repo_state
                        current_save_task = await self._resolve_commit_conflict_using_local_changes(
                            new_repo_state, project
                        )
                        if current_save_task is not None:
                            new_file_change_event_task = asyncio.create_task(self.want_to_save_flag.wait())
                    else:
                        # FIXME: actually implement this
                        logger.debug("Decided to handle remote commit conflict by using REMOTE changes")
                        # # not too hard to implement, something like this (same code as below)
                        # message = pending_messages[-1]
                        # await self._process_new_repo_state_message(message, project)
                        # pending_messages.clear()
                        raise NotImplementedError()
                    conflict_version = None
                    continue

                # if there is any pending save event, we just need to wait for that.
                if current_save_task is not None:
                    logger.debug("## Waiting for pending save task to finish")
                    continue

                if self.want_to_save_flag.is_set():
                    logger.debug("### Sending save event to server")
                    # actually handle the save
                    current_save_task = await self._handle_save(
                        self._last_remote_repo_state,
                        project,
                        is_forced=False,
                        last_save_version=last_clean_save_version,
                    )
                    if current_save_task is not None:
                        new_file_change_event_task = asyncio.create_task(self.want_to_save_flag.wait())
                    # go wait for more things to happen
                    continue

                # FIXME: there is a race condition here, but it is hard to fix
                #  If we have received some new state from the server, and *right* as we go to apply it, the user saves
                #  The *only* reliable way around this is to lock the entirety of the user's repo while we are syncing
                #  However, this effectively requires an IDE integration...
                #  An alternative implementation would be to lock the git index, then remove write permissions from each
                #  file that we were going to modify.  That would work, but potentially be annoying to get transient
                #  permission errors while you are saving

                # at this point, we know:
                # 1. we are not conflicted
                # 2. we are not saving
                # 3. we don't even want to save
                # so let's process any message from the server that says that our local state should change
                logger.debug("## Processing any new remote state messages")
                latest_message = _get_most_recent_remote_state_message(new_remote_state_messages)
                new_remote_state_messages.clear()
                if latest_message is not None:
                    logger.debug("### Processing new remote state message")
                    is_different_commit = latest_message.commit_hash != self._last_remote_repo_state.commit_hash
                    if latest_message.version > last_clean_save_version or (
                        latest_message.version == last_clean_save_version and is_different_commit
                    ):
                        logger.debug(
                            "### Remote state version >= local state version and is different so applying new remote state"
                        )
                        await self._process_new_repo_state_message(latest_message, project, should_apply=True)

                        # make sure we remember where our branch is
                        logger.debug("### Saving previous branch name")
                        await self._save_previous_branch_name(self._last_remote_repo_state)

                        logger.debug("### Checking if branch has changed locally")
                        # we now also need to check whether the branch has changed locally
                        is_new_branch = self._last_remote_repo_state.branch_name != starting_state.branch_name
                        # and if so, return -- we're done syncing this branch, and we've clearly selected a new one as a result of the remote sync event
                        if is_new_branch:
                            logger.debug("New branch received from remote, re-syncing")
                            return
                    elif latest_message.version == last_clean_save_version:
                        logger.debug(
                            "### Latest remote state is same as our current version. Updating last remote state."
                        )
                        await self._process_new_repo_state_message(latest_message, project, should_apply=False)
                    else:
                        logger.debug("### Ignoring latest remote state -- is <= our current version")

                # and now we're done, so just loop and do it all over again!
        finally:
            logger.debug("### Exiting main sync loop")
            # for sanity, cancel any outstanding task(s)
            await safe_cancel_and_wait_for_cleanup(next_message_task)
            if new_file_change_event_task is not None:
                await safe_cancel_and_wait_for_cleanup(new_file_change_event_task)
            if current_save_task is not None:
                await safe_cancel_and_wait_for_cleanup(current_save_task)
                current_save_task = None

    async def _resolve_commit_conflict_using_local_changes(
        self, new_remote_repo_state: VersionedLocalRepoState, project: Project
    ) -> asyncio.Task[AppliedSaveMessage | FailedToSaveMessage] | None:
        logger.debug("Decided to handle remote commit conflict by using LOCAL changes")
        current_save_task = await self._handle_save(new_remote_repo_state, project, is_forced=True)
        return current_save_task

    async def _definitely_get_current_branch_name(self) -> Optional[str]:
        repo = LocalGitRepo(self.local_sync_repo_path)
        while True:
            try:
                current_local_branch_name = await get_branch_name(repo, is_error_logged=False)
                break
            except RunCommandError as e:
                if await is_detached_head(repo):
                    current_local_branch_name = None
                    break
                else:
                    logger.debug(f"Failed to get branch name because: {e}")
                    await asyncio.sleep(0.1)
        return current_local_branch_name

    # FIXME: someday we could actually prompt the user. For now, just assuming that they want the local changes
    #  Remember that, because asking the user can block, we need to be mindful about new remote and local changes
    async def _prompt_user_about_commit_conflict(self) -> bool:
        logger.warning("You made changes locally while syncing with the server -- what do you want to do?")
        is_using_local_changes = True
        return is_using_local_changes

    # FIXME: we could be smarter here about prompting the user when they have differences with the remote branch
    async def _handle_conflicted_branch(
        self, starting_state: LocalRepoState, remote_state_description: str, project: Project
    ) -> str:
        logger.debug("Decided to handle remote branch conflict by using LOCAL changes")
        return "LOCAL"

    async def _process_new_repo_state_message(
        self, message: NewRemoteRepoStateMessage, project: Project, should_apply: bool = True
    ) -> None:
        logger.info(f"processing message {type(message).__name__} with version={message.version}")
        logger.trace(str(message))
        self.current_user_message = message

        # received a new repo state from the remote agent, try to update local state to match
        new_repo_state = VersionedLocalRepoState(
            branch_name=message.branch_name,
            version=message.version,
            commit_hash=message.commit_hash,
            repo_operation=message.repo_operation,
        )
        if new_repo_state == self._last_remote_repo_state:
            logger.debug("New remote repo state is the same as the last remote repo state. Nothing to do.")
        else:
            self._last_remote_repo_state = new_repo_state
            if should_apply:
                await self._on_new_remote_repo_state(new_repo_state, project)

        logger.info(f"finished processing message {type(message).__name__}")
        self.messages = (*self.messages, message)
        self.current_message = None

    async def _on_new_remote_repo_state(self, new_repo_state: VersionedLocalRepoState, project: Project) -> None:
        # update current saved local repo state, to match the remote state
        file_watcher = self.get_file_watcher()
        try:
            async with self._get_local_repo_for_sync() as repo:
                # disable file watcher here so that we don't get messages while we are setting the state
                async with file_watcher.disable():
                    await self._local_force_checkout(
                        repo, new_repo_state.commit_hash, new_repo_state.branch_name, project
                    )
                    if isinstance(new_repo_state.repo_operation, CleanRepoOperation):
                        await self._apply_new_clean_remote_repo_state(repo, new_repo_state.repo_operation)
                    elif isinstance(new_repo_state.repo_operation, ConflictedRepoOperation):
                        await self._apply_new_conflicted_remote_repo_state(repo, new_repo_state.repo_operation)
                    else:
                        raise ValueError("New remote repo state is not clean or conflicted")
        except Exception as e:
            logger.error(f"Error overwriting local repo with new state: {e}")
            raise

    async def _apply_new_clean_remote_repo_state(
        self, repo: LocalGitRepo, clean_repo_operation: CleanRepoOperation
    ) -> None:
        logger.debug("Applying new clean remote repo state locally")
        try:
            if clean_repo_operation.staged_diff:
                await apply_patch_via_git_with_conflict_markers(
                    repo, clean_repo_operation.staged_diff, is_error_logged=False
                )
                await repo.run_git(["add", "."])
            if clean_repo_operation.unstaged_diff:
                await apply_patch_via_git_with_conflict_markers(
                    repo, clean_repo_operation.unstaged_diff, is_error_logged=False
                )
        except RunCommandError as e:
            raise ValueError("Failed to apply diff") from e

    async def _apply_new_conflicted_remote_repo_state(
        self, repo: LocalGitRepo, conflicted_repo_operation: ConflictedRepoOperation
    ) -> None:
        logger.debug("Applying new conflicted remote repo state locally")
        await asyncio.gather(
            *[
                anyio.Path(repo.base_path / path).write_bytes(content)
                for path, content in conflicted_repo_operation.modified_file_contents_by_path.items()
            ],
            *[
                anyio.Path(repo.base_path / ".git" / path).write_bytes(content)
                for path, content in conflicted_repo_operation.special_git_file_contents_by_path.items()
            ],
            anyio.Path(repo.base_path / ".git" / "index").write_bytes(conflicted_repo_operation.index_content),
            write_blob_content_by_hash(repo, conflicted_repo_operation.blob_content_by_hash),
        )

    async def _local_force_checkout(
        self, repo: LocalGitRepo, git_hash: str, branch_name: str, project: Project
    ) -> None:
        logger.debug("Force checkout locally")

        try:
            await repo.run_git(["fetch", project.backend_repo_url, git_hash], retry_on_git_lock_error=True)
            # clean our state
            logger.debug("force checkout: resetting hard")
            await repo.run_git(["reset", "--hard"], retry_on_git_lock_error=True)
            # remove untracked files
            logger.debug("force checkout: cleaning")
            await repo.run_git(["clean", "-fd"], retry_on_git_lock_error=True)
            # checkout the new commit in detached head state (we may re-attach to a branch later, see below)
            #  we need to do this first so we can update the local branch state to match the remote branch state below
            logger.debug("force checkout: checking new commit")
            await repo.run_git(["checkout", git_hash], retry_on_git_lock_error=True)

            # FIXME: this fetch seems entirely pointless... why didn't we just fetch what we needed above?
            #  morever, our other async work ought to be done in parallel while doing the fetch
            #  because this work is in the critical path

            # Update the local branch state to match the remote branch state
            # fetch the branch from the backend
            # NOTE: this will set the FETCH_HEAD ref, which we can use to re-attach to the branch below
            logger.debug(f"force checkout: fetching branch {branch_name} from backend at {project.backend_repo_url}")
            await repo.run_git(["fetch", project.backend_repo_url, branch_name], retry_on_git_lock_error=True)
            # update the local branch to match the remote branch
            logger.debug(f"force checkout: updating local branch {branch_name} to match remote branch")
            await repo.run_git(["branch", "-f", branch_name, "FETCH_HEAD"], retry_on_git_lock_error=True)

            # if `git_hash` is the same as the updated branch, re-attach
            # otherwise user is synced to different commit to the current branch commit, so leave in detached head state
            branch_commit_hash = await repo.run_git(["rev-parse", branch_name], retry_on_git_lock_error=True)
            logger.debug(f"force checkout: {branch_commit_hash=} {git_hash=}")
            if branch_commit_hash == git_hash:
                logger.debug("force checkout: re-attaching to branch")
                await repo.run_git(["checkout", branch_name], retry_on_git_lock_error=True)
        except RunCommandError:
            # FIXME: we should handle this nicely.
            logger.error("force checkout: failed to checkout new commit.")
            raise
        logger.debug(f"force checkout done {git_hash}")

    async def _handle_save(
        self,
        remote_repo_state: VersionedLocalRepoState,
        project: Project,
        is_forced: bool,
        last_save_version: Optional[int] = None,
    ) -> asyncio.Task[AppliedSaveMessage | FailedToSaveMessage] | None:
        logger.debug(f"New local save message {self.local_sync_repo_path=}")

        # clear the flags, since we are saving now
        self.want_to_save_flag.clear()

        # get our current state
        current_local_repo_state = await self._get_current_local_repo_state()

        # return early if there's nothing to do
        if not is_forced and is_local_repo_states_equal(current_local_repo_state, remote_repo_state):
            logger.debug("No changes to local repo state compared to remote state")
            logger.debug(f"current local repo state:\n{current_local_repo_state=}")
            logger.debug(f"remote repo state:\n{remote_repo_state=}")
            current_save_task = None
        else:
            # if we have a new commit or branch
            if remote_repo_state.commit_hash != current_local_repo_state.commit_hash:
                # we need to push this to the backend so it has access to it
                # and we want to do this BEFORE sending the message (so that the backend doesn't need to worry about not having the commit)
                await self._push_new_commit_to_backend(
                    current_local_repo_state.commit_hash, current_local_repo_state.branch_name, project
                )

            version = (
                remote_repo_state.version
                if last_save_version is None
                else max(last_save_version, remote_repo_state.version)
            )
            message = NewLocalRepoStateMessage(
                client_id=self.client_id,
                project_id=project.id,
                client_info=get_client_info(),
                branch_name=current_local_repo_state.branch_name,
                version=version,
                commit_hash=current_local_repo_state.commit_hash,
                repo_operation=current_local_repo_state.repo_operation,
            )
            current_save_task = create_clean_task(self._send_message(message))
        return current_save_task

    async def _get_current_local_repo_state(self) -> LocalRepoState:
        logger.debug("Getting current local repo state")
        async with self._get_local_repo_for_sync() as repo:
            logger.debug("Getting branch name")
            try:
                branch_name = await get_branch_name(repo, is_error_logged=False)
            except RunCommandError:
                if await is_detached_head(repo):
                    branch_name = None
                else:
                    raise

            if branch_name is None:
                # we are in a detached head state, but we still need to let the backend know what branch we are working on
                # so we assume it is the branch from the last remote state, if it exists
                branch_name = await self._load_previous_branch_name(repo)
                if branch_name is None:
                    raise ActiveBranchUnknownError(
                        "Active branch unknown. This happens if you are started in a detached head state, make sure to checkout a branch and try again."
                    )
            logger.debug(f"Got branch name: {branch_name=}")

            # FIXME: much of the below could be run in parallel...
            #  but also, it's not totally clear that this code is safe. We need some locks here if we don't want to go crazy...
            #  doing it in parallel at least makes it slightly safer in practice :-P
            commit_hash = await repo.head_hash()
            conflict_type = await get_conflict_type_from_computing_environment(repo)
            if conflict_type is not None:
                logger.debug(f"In conflicted state: {conflict_type=}")
                index_content = await anyio.Path(repo.base_path / ".git" / "index").read_bytes()
                blob_content_by_hash = await get_unmerged_and_staged_blob_contents_by_hash(repo)
                modified_file_contents_by_path = await get_modified_file_contents_by_path(repo)
                special_git_file_contents_by_path = await get_special_git_file_contents_by_path_for_conflict_type(
                    repo, conflict_type
                )
                return LocalRepoState(
                    branch_name=branch_name,
                    commit_hash=commit_hash,
                    repo_operation=ConflictedRepoOperation(
                        blob_content_by_hash=FrozenDict(blob_content_by_hash),
                        index_content=index_content,
                        modified_file_contents_by_path=FrozenDict(modified_file_contents_by_path),
                        conflict_type=conflict_type,
                        special_git_file_contents_by_path=FrozenDict(special_git_file_contents_by_path),
                    ),
                )

            logger.debug("No conflicts detected so getting staged, unstaged, and combined diffs.")
            staged_diff, unstaged_diff, combined_diff = await get_staged_unstaged_and_combined_diffs(repo)
            return LocalRepoState(
                branch_name=branch_name,
                commit_hash=commit_hash,
                repo_operation=CleanRepoOperation(
                    staged_diff=staged_diff,
                    unstaged_diff=unstaged_diff,
                    combined_diff=combined_diff,
                ),
            )

    async def _push_new_commit_to_backend(
        self, commit_hash: str, branch_name: str, project: Project, target_branch_name: Optional[str] = None
    ) -> None:
        """Push commit to backend.

        If `target_branch_name` is provided, we will also push both branch_name and target_branch_name. This can
        be used to make sure that these branches exist on the backend (e.g. when syncing a new branch).
        """
        logger.debug(f"Pushing new commit to backend: {commit_hash} {branch_name=}")

        async with self._get_local_repo_for_sync() as repo:
            # the branch we push to on the backeend
            # we use `self.client_id` since we want to push to a temporary branch on the backend
            #  the backend will then handle merging this into the actual branch (or not if things our out-of-date, etc)
            backend_working_branch_name = f"{self.client_id}/{branch_name}"
            # push the new commit to the backend
            # we need the `--force` flag because the branch may already exist on the backend, and we want to overwrite it
            #  (any previous commits on pushed on the branch will still exist on the backend as detached commits)
            await repo.run_git(
                [
                    "push",
                    project.backend_repo_url,
                    "--force",
                    f"{commit_hash}:refs/heads/{backend_working_branch_name}",
                    *([f"refs/heads/{branch_name}"] if target_branch_name else []),
                    *(
                        [f"refs/heads/{target_branch_name}"]
                        if target_branch_name and target_branch_name != branch_name
                        else []
                    ),
                ]
            )

    @asynccontextmanager
    async def _get_local_repo_for_sync(self) -> AsyncGenerator[LocalGitRepo, None]:
        async with self._local_repo_lock:
            async with self._local_repo_git_lock():
                yield LocalGitRepo(base_path=self.local_sync_repo_path)

    @asynccontextmanager
    async def _local_repo_git_lock(self) -> AsyncGenerator[None, None]:
        """Context manager to check and wait for git index lock to be free.

        This function checks if the git index lock file exists in the repo,
        and waits until it's free before proceeding. This prmessages conflicts
        when multiple operations try to modify the git index at the same time.

        Git creates and removes the index.lock file itself, so this context manager
        only waits for the lock to be free and doesn't attempt to create or remove it.
        """
        # Path to the git index lock file using anyio.Path to avoid blocking
        lock_file_path = anyio.Path(self.local_sync_repo_path / ".git" / "index.lock")

        # Wait until the index.lock file doesn't exist
        max_retries = 50
        retry_count = 0
        retry_delay = 0.1  # seconds
        while await lock_file_path.exists() and retry_count < max_retries:
            logger.debug(f"Git index lock file exists at {lock_file_path}, waiting...")
            await asyncio.sleep(retry_delay)
            retry_count += 1
            # delay backoff with a cap at 1 second
            retry_delay = min(retry_delay + 0.1, 1.0)

        if await lock_file_path.exists():
            logger.error(f"Git index lock file still exists after {max_retries} retries")
            # We'll continue anyway, which will probably fail but produce a useful error message

        # We don't create the lock ourselves - git will handle that
        # This context manager is just waiting until no lock exists before proceeding
        yield

    async def close(self) -> None:
        logger.info("Closing local client service")
        self._is_done = True
        exception_types_to_ignore = (ClientResponseError,)
        if self.run_task is not None:
            logger.debug("Cancelling run task")
            await safe_cancel_and_wait_for_cleanup(self.run_task, exception_types_to_ignore=exception_types_to_ignore)
        if self._file_watcher is not None:
            logger.debug("Closing file watcher")
            self._file_watcher.close()
        if self._file_watcher_message_reader_task is not None:
            logger.debug("Cancelling file watcher message reader task")
            await safe_cancel_and_wait_for_cleanup(self._file_watcher_message_reader_task)
        remove_project_from_lock_file(self.local_sync_repo_path)
        logger.info("Local client service closed")


def _process_next_message_from_server(
    next_message_task: asyncio.Task[LocalSyncServerMessage],
) -> Optional[NewRemoteRepoStateMessage]:
    message = next_message_task.result()
    # we always just stick these in the message queue. They are processed below
    if isinstance(message, NewRemoteRepoStateMessage):
        assert not isinstance(message, SyncedMessage), "Why did we get a second sync message..."
        logger.debug("Enqueued new remote repo state message")
        return message
    # the rest of the messages can be safely ignored for now
    elif isinstance(message, NewProjectMessage):
        return None
    # ...but we do so explicitly, in case we accidentally make a new type and forget to handle it
    else:
        raise Exception(f"Unexpected message type: {type(message)}")


async def _get_target_branch_name(
    local_state: LocalRepoState,
    remote_state: Optional[VersionedLocalRepoState],
    local_sync_repo_path: Path,
) -> str:
    """
    The point of this function is to figure out where we are branching *from*

    This is not actually a well-defined thing in git, but it's really convenient, because you're almost always
    thinking about the most recent branch point.

    The user can set this later if we got it wrong, so it's not a huge deal.
    """
    repo = LocalGitRepo(base_path=local_sync_repo_path)
    branch_names = await get_most_recent_sibling_branch_of_branch(repo, local_state.branch_name)
    if branch_names is None or len(branch_names) == 0:
        return local_state.branch_name
    if remote_state is not None and remote_state.branch_name in branch_names:
        return remote_state.branch_name
    return sorted(branch_names)[0]


def _get_most_recent_remote_state_message(
    messages: List[NewRemoteRepoStateMessage],
) -> Optional[NewRemoteRepoStateMessage]:
    if len(messages) == 0:
        return None
    return sorted(messages, key=lambda x: x.version)[-1]
