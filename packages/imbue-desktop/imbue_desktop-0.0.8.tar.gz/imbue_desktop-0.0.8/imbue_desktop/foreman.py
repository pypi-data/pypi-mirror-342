"""
Integration with imbue-foreman (our central server).

"""
import asyncio
import time
from typing import Optional
from typing import Tuple

import aiohttp
from loguru import logger

DEFAULT_FOREMAN_URL = "https://imbue-foreman.fly.dev"
MAX_WAITING_TIME_SECONDS_NEW_INSTANCE = 64
# For old instances, we don't wait that long because they are already running.
# If we can't reach them within a few seconds, it probably means they are down and we need a new one.
MAX_WAITING_TIME_SECONDS_OLD_INSTANCE = 2


class ForemanUnexpectedResponseError(Exception):
    pass


class SculptorInstanceNotReadyInTimeError(Exception):
    pass


class TooManyInstancesCreatedError(Exception):
    pass


async def get_or_create_sculptor_server(api_key: str, foreman_url: str, is_new_instance_forced: bool) -> Optional[str]:
    """
    Negotiates a scultptor instance with foreman and waits until it's ready.

    (Can be an existing one or a new one, we don't know.)

    """
    headers = {"Authorization": f"Bearer {api_key}"}
    base_url = foreman_url.rstrip("/")
    instance_url: Optional[str] = None
    async with aiohttp.ClientSession(headers=headers) as session:
        logger.info("Getting sculptor instance from foreman...")
        for is_new_enforced_stage in (False, True):
            if is_new_instance_forced and not is_new_enforced_stage:
                logger.info("Skipping old instance because we want a new one.")
                continue
            result = await _get_or_create_sculptor_server(session, base_url, is_new_enforced_stage)
            if result is None:
                logger.info("Foreman didn't give us an instance.")
                return None
            instance_url, is_newly_spawned = result
            logger.info("Waiting until the instance is ready...")
            time_to_wait = (
                MAX_WAITING_TIME_SECONDS_NEW_INSTANCE if is_newly_spawned else MAX_WAITING_TIME_SECONDS_OLD_INSTANCE
            )
            try:
                await _wait_for_the_instance_to_be_ready(session, instance_url, time_to_wait)
            except SculptorInstanceNotReadyInTimeError:
                if not is_newly_spawned:
                    logger.info("An old instance is not reachable. Trying to get a fresh one.")
                    continue
                raise
            break
        assert instance_url is not None
        logger.info("Instance is ready.")
        return instance_url


async def _get_or_create_sculptor_server(
    session: aiohttp.ClientSession, base_url: str, is_new_enforced: bool = False
) -> Optional[Tuple[str, bool]]:
    try:
        url = f"{base_url}/ensure-instance"
        if is_new_enforced:
            url += "?is_new_enforced=true"
        response = await session.post(url)
        response.raise_for_status()
    except aiohttp.ClientConnectionError as e:
        # We're robust towards Foreman not being available at all and to auth errors.
        # We should raise for all other cases, though.
        # (Because it typically means we need to fix something.)
        logger.info(f"Failed to negotiate sculptor instance with foreman: {e}")
        return None
    except aiohttp.ClientResponseError as e:
        if e.status in (401, 403):
            logger.info(f"Failed to negotiate sculptor instance with foreman: {e}")
            return None
        if e.status == 429:
            raise TooManyInstancesCreatedError(f"Attempted to create too many instances: {e}")
        raise
    try:
        instance_data = await response.json()
        logger.info(f"Got sculptor instance data from foreman: {instance_data}")
        instance_url = instance_data["url"]
        is_newly_spawned = instance_data["is_newly_spawned"]
    except aiohttp.ContentTypeError:
        logger.info(f"Failed to get URL from foreman: {response.text}")
        raise ForemanUnexpectedResponseError(f"Failed to get URL from foreman: {response.text}")
    return instance_url, is_newly_spawned


async def _wait_for_the_instance_to_be_ready(
    session: aiohttp.ClientSession, instance_url: str, time_to_wait: int
) -> None:
    """
    Waits until the instance is ready.

    """
    started_at = time.monotonic()
    while True:
        try:
            response = await session.get(f"{instance_url}/api/ping/", timeout=5)
            response.raise_for_status()
            return
        except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError):
            logger.info("Still waiting...")
            # This is a newly spawned instance and it takes it a bit more time to be ready.
            await asyncio.sleep(2)
            if time.monotonic() - started_at > time_to_wait:
                raise SculptorInstanceNotReadyInTimeError("Timed out waiting for the instance to be ready.")
            continue
