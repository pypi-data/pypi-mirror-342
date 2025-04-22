from functools import lru_cache
from pathlib import Path
from typing import Optional

import platformdirs


@lru_cache(maxsize=None)
def ensure_app_data_dir() -> Path:
    return Path(platformdirs.user_data_path("imbue", ensure_exists=True))


def get_api_token() -> Optional[str]:
    token_path = ensure_app_data_dir() / "api_token.txt"
    if token_path.exists():
        return token_path.read_text()
    else:
        return None


def set_api_token(token: str) -> None:
    (ensure_app_data_dir() / "api_token.txt").write_text(token)
