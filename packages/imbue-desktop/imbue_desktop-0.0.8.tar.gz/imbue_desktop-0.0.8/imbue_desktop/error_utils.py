import os
from pathlib import Path
from typing import Optional
from typing import cast

import jwt
import sentry_sdk
from loguru import logger
from sentry_sdk.attachments import Attachment
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.types import Event
from sentry_sdk.types import Hint

from imbue_core.error_utils import get_traceback_with_vars
from imbue_core.git import is_path_in_git_repo
from imbue_core.sentry_loguru_handler import SentryBreadcrumbHandler
from imbue_core.sentry_loguru_handler import SentryEventHandler
from imbue_core.sentry_loguru_handler import SentryLoguruLoggingLevels

CRAFTY_DESKTOP_SENTRY_DSN = (
    "https://59304833d290f6a7cee0692a12ed8c95@o4504335315501056.ingest.us.sentry.io/4509130267623424"
)


def sentry_before_send_hook(event: Event, hint: Hint) -> Optional[Event]:
    """used to add extra info or filter events before sending."""

    expected_attachments = []

    # TODO: if we have a log file, we should log it too

    tb_with_vars = get_traceback_with_vars()
    hint["attachments"].append(Attachment(tb_with_vars.encode(), filename="traceback_with_variables.txt"))
    expected_attachments.append("traceback_with_variables.txt")

    # record the names of the expected attachments just in case there's any weirdness about attachments not showing up
    event["extra"]["expected_attachments"] = str(expected_attachments)

    return event


class InvalidAPIKeyError(Exception):
    pass


def get_username_for_sentry(api_key: Optional[str]) -> str:
    if api_key is None:
        assert "CRAFTY_USERNAME" in os.environ, "if api_key is not provided, CRAFTY_USERNAME must be set"
        return os.environ["CRAFTY_USERNAME"]
    try:
        decoded_jwt = jwt.decode(api_key, options={"verify_signature": False})
        return cast(str, decoded_jwt["user_email"])
    except jwt.DecodeError as e:
        raise InvalidAPIKeyError("Invalid API key provided.") from e


def setup_sentry(username: str) -> None:
    assert (
        "SENTRY_DSN" not in os.environ
    ), "SENTRY_DSN should not be set in the environment, otherwise it overrides the passed in value confusingly"

    sentry_sdk.init(
        dsn=CRAFTY_DESKTOP_SENTRY_DSN,
        sample_rate=1.0,
        traces_sample_rate=1.0,
        # required for `logger.error` calls to include stacktraces
        attach_stacktrace=True,
        # note this will capture unhandled exceptions even if not explicitly logged, among other things
        # https://docs.sentry.io/platforms/python/integrations/default-integrations/
        default_integrations=True,
        # this doesn't affect the default integrations, but prevents any other ones from being added automatically
        auto_enabling_integrations=False,
        integrations=[],
        disabled_integrations=[
            # this only adds hooks to subprocess and httplib, which imo just adds noisy breadcrumbs.
            StdlibIntegration()
        ],
        # may want to get more restrictive about this in the future
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/
        send_default_pii=True,
        # sentry has a max payload size of 1MB, so we can't make this infinite
        max_value_length=100_000,
        add_full_stack=True,
        before_send=sentry_before_send_hook,
        # TODO: need to figure out how to do releases/versioning here.
        # users won't have our git repo so we can't do the git-commit based versioning we use in the backend
        # release=crafty_version,
        # default is 100; can't make it too large because total event size must be <1MB
        max_breadcrumbs=1000,
        # end users should be running this via a pip package, so not in a repo. our devs will be running from our repo.
        environment="development" if is_path_in_git_repo(Path(__file__)) else "production",
    )
    logger.info("Sentry initialized")

    # capture loguru errors/exceptions with a custom handler
    error_level: int = SentryLoguruLoggingLevels.ERROR.value
    logger.add(SentryEventHandler(level=error_level), level=error_level, diagnose=False)
    # capture lower level loguru messages to add as breadcrumbs on events
    # the extra info is not helpful here and makes the breadcrumbs larger; they're still available in the log file attachment
    breadcrumb_level: int = SentryLoguruLoggingLevels.INFO.value
    logger.add(
        SentryBreadcrumbHandler(level=breadcrumb_level, strip_extra=True), level=breadcrumb_level, diagnose=False
    )

    sentry_sdk.set_user({"username": username})
