from datetime import datetime, timezone
import os
from typing import Optional


def to_datetime(value: str) -> Optional[datetime]:
    if value is None:
        return None
    if value.startswith("0001-01-01"):
        return None
    return datetime.fromisoformat(value[:19] + "Z")


def guard_dir(dir: str) -> None:
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Path {dir} is not a dir")


def guard_path(path: str) -> None:
    if not os.access(path, os.R_OK):
        raise FileNotFoundError(f"Path {path} not found")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Path {path} is not a file")


def guard_utc_datetime(dt: Optional[datetime]) -> None:
    if dt is None:
        return
    if type(dt) is not datetime or dt.tzinfo != timezone.utc:
        raise ValueError("released is neither None or a UTC timezone")
