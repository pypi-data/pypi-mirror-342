import uuid
from pathlib import Path
from typing import Optional

import toml

from imbue_desktop.errors import NoAPIKeyError
from imbue_desktop.errors import NoURLError

IMBUE_TOML_PATH = Path("~/.imbue.toml").expanduser()


def read_imbue_toml() -> dict:
    if not IMBUE_TOML_PATH.exists():
        return {}
    return toml.load(IMBUE_TOML_PATH)


def write_to_imbue_toml(key: str, value: str) -> None:
    if not IMBUE_TOML_PATH.exists():
        # create empty dict
        imbue_toml_dict = {}
    else:
        imbue_toml_dict = toml.load(IMBUE_TOML_PATH)
    imbue_toml_dict[key] = value
    with open(IMBUE_TOML_PATH, "w") as f:
        toml.dump(imbue_toml_dict, f)


def get_api_key_from_imbue_toml() -> str:
    imbue_toml = read_imbue_toml()
    api_key: Optional[str] = imbue_toml.get("api_key", None)
    if api_key is None:
        raise NoAPIKeyError()
    return api_key


def get_url_from_imbue_toml(is_error_raised_if_not_present: bool = True) -> Optional[str]:
    imbue_toml = read_imbue_toml()
    url: Optional[str] = imbue_toml.get("url", None)
    if url is None and is_error_raised_if_not_present:
        raise NoURLError()
    return url


def get_or_create_machine_id() -> str:
    imbue_toml = read_imbue_toml()
    machine_id: Optional[str] = imbue_toml.get("machine_id", None)
    if machine_id is None:
        machine_id = str(uuid.uuid4()).replace("-", "")[:16]
        write_to_imbue_toml("machine_id", machine_id)
    return machine_id
