import contextlib
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import TypeVar
from typing import Union

import attr
import psutil
import typer

from imbue_desktop.local_sync_client.data_types import LocalRepoState
from imbue_desktop.local_sync_client.data_types import VersionedLocalRepoState

T = TypeVar("T")


def only(x: Iterable[T]) -> T:
    try:
        (value,) = x
    except ValueError as e:
        message = "Expected exactly one value"
        if isinstance(x, Sequence):
            with contextlib.suppress():
                message += f" but got {len(x)} {x[:3]=}"
        raise ValueError(message) from e

    return value


async def get_project_name_from_local_repo(repo_path: Path) -> str:
    return repo_path.name


def is_local_repo_states_equal(
    state_1: Union[LocalRepoState, VersionedLocalRepoState], state_2: Union[LocalRepoState, VersionedLocalRepoState]
) -> bool:
    """Checks two local repo states are equal.

    This is a convenience method to handle equality between LocalRepoState and VersionedLocalRepoState.
    """
    if type(state_1) is type(state_2):
        return state_1 == state_2
    # different types so check parent class attribues are equal
    for field in attr.fields(LocalRepoState):
        if getattr(state_1, field.name) != getattr(state_2, field.name):
            return False
    return True


def get_pid_file_path() -> Path:
    """Get the path to the pid file for the local sync client."""
    # use the default temp dir for the OS
    return Path(tempfile.gettempdir()) / "local_sync_client.pid"


def is_client_already_running(local_sync_repo_path: Path) -> bool:
    """Check if another instance of the local sync client is already running."""
    pid_file_path = get_pid_file_path()
    if not pid_file_path.exists():
        return False

    project_pid = None
    with open(pid_file_path, "r") as f:
        for line in f.readlines():
            pid, path_str = line.split()
            if path_str == local_sync_repo_path.as_posix():
                project_pid = int(pid)
                break

    if project_pid is None:
        return False

    # check if the process is running
    try:
        process = psutil.Process(project_pid)
        if process.is_running():
            # Get the command line arguments
            cmdline = process.cmdline()
            # Check if this is actually a local sync client process
            # TODO we should check for some more specific patterns, for now we just check if it's a python process
            if any("python" in arg for arg in cmdline):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # Process doesn't exist or we can't access its info
        pass
    return False


def add_project_to_lock_file(local_sync_repo_path: Path) -> None:
    """Write the pid of the current process to the pid file."""
    pid_file_path = get_pid_file_path()
    our_pid = os.getpid()
    local_repo_path_str = local_sync_repo_path.as_posix()

    if not pid_file_path.exists():
        # create the file with the current pid
        with open(pid_file_path, "w") as f:
            f.write(f"{our_pid} {local_repo_path_str}")
        return

    new_contents = []
    with open(pid_file_path, "r") as f:
        for line in f.readlines():
            _, path_str = line.split()
            if path_str == local_repo_path_str:
                new_contents.append(f"{our_pid} {local_repo_path_str}")
            else:
                new_contents.append(line)

    with open(pid_file_path, "w") as f:
        f.writelines(new_contents)


def remove_project_from_lock_file(local_sync_repo_path: Path) -> None:
    """Remove the pid from the pid file for the given project."""
    pid_file_path = get_pid_file_path()

    if not pid_file_path.exists():
        return

    local_repo_path_str = local_sync_repo_path.as_posix()
    new_contents = []
    with open(pid_file_path, "r") as f:
        for line in f.readlines():
            _, path_str = line.split()
            if path_str == local_repo_path_str:
                continue
            new_contents.append(line)

    with open(pid_file_path, "w") as f:
        f.writelines(new_contents)


def validate_branch_at_launch(
    local_sync_repo_path: Path, branch_name: Optional[str], reset_to_remote: bool = False
) -> None:
    if branch_name is None:
        _assert_on_a_branch(local_sync_repo_path)
    else:
        _checkout_branch_locally(local_sync_repo_path, branch_name, reset_to_remote)


def _checkout_branch_locally(local_sync_repo_path: Path, branch_name: str, reset_to_remote: bool = False) -> None:
    typer.secho(
        "You have specified a branch during launch. Configuring your local repo to match..", fg=typer.colors.YELLOW
    )

    typer.secho("Checking for uncommitted changes", fg=typer.colors.YELLOW)
    has_uncommitted_changes = False
    try:
        subprocess.run(["git", "status", "--porcelain"], cwd=local_sync_repo_path, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        has_uncommitted_changes = True

    if has_uncommitted_changes:
        typer.secho(
            f"Local sync repo {local_sync_repo_path} has uncommitted changes.",
            fg=typer.colors.RED,
        )
        if not typer.confirm("Discard these changes and continue?"):
            typer.secho(
                "Aborting. Please commit or stash your changes before relaunching the local sync client.",
                fg=typer.colors.RED,
            )
            typer.Abort()
        try:
            subprocess.run(["git", "reset", "--hard"], cwd=local_sync_repo_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            typer.secho(
                "Failed to reset local branch. Please check your repo is in a good state and try again.",
                fg=typer.colors.RED,
            )
            typer.Abort()

    typer.secho(f"Checking out branch: {branch_name}", fg=typer.colors.YELLOW)
    try:
        subprocess.run(["git", "checkout", branch_name], cwd=local_sync_repo_path, check=True, capture_output=True)
        typer.secho(f"Successfully checked out branch: {branch_name}", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho(
            f"Failed to checkout branch: {branch_name}. Please check that the branch exists and you have permission to access it.",
            fg=typer.colors.RED,
        )
        typer.Abort()

    if not reset_to_remote:
        return

    # check if repo has remote, and if so, reset local to match remote branch
    try:
        typer.secho("Checking if remote exists", fg=typer.colors.YELLOW)
        subprocess.run(
            ["git", "remote", "get-url", "origin"], cwd=local_sync_repo_path, check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        typer.secho("No remote found, so not resetting local to match remote branch", fg=typer.colors.YELLOW)
        return

    # check that remote branch exists
    try:
        typer.secho(f"Checking if remote branch {branch_name} exists", fg=typer.colors.YELLOW)
        subprocess.run(
            ["git", "rev-parse", "--verify", f"origin/{branch_name}"],
            cwd=local_sync_repo_path,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        typer.secho(
            f"Remote branch {branch_name} does not exist. Skipping resetting to remote branch.",
            fg=typer.colors.YELLOW,
        )
        return

    typer.secho(f"Resetting local to match remote branch {branch_name}", fg=typer.colors.YELLOW)
    try:
        subprocess.run(
            ["git", "fetch", "origin", branch_name], cwd=local_sync_repo_path, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "reset", "--hard", f"origin/{branch_name}"],
            cwd=local_sync_repo_path,
            check=True,
            capture_output=True,
        )
        typer.secho(f"Successfully reset local to match remote branch {branch_name}", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho(f"Failed to reset local to match remote branch: {branch_name}", fg=typer.colors.RED)
        # we can still continue, but ask the user if they want to continue
        if not typer.confirm("Continue anyway?"):
            typer.Abort()


def _assert_on_a_branch(local_sync_repo_path: Path) -> None:
    try:
        output = subprocess.run(
            ["git", "branch", "--show-current"], cwd=local_sync_repo_path, check=True, capture_output=True
        )
        current_branch = output.stdout.decode().strip()
        if current_branch != "":
            typer.secho(f"Running on branch: {current_branch}", fg=typer.colors.GREEN)
            return
    except subprocess.CalledProcessError:
        pass

    typer.secho(
        f"Local repo {local_sync_repo_path} is not on a branch. Please checkout a branch and try again.",
        fg=typer.colors.RED,
    )
    typer.Abort()
