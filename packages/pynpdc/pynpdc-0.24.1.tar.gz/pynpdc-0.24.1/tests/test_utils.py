from datetime import datetime, timezone
import os
import pytest
import unittest
import uuid
from pynpdc.utils import guard_dir, guard_path, guard_utc_datetime


class TestGuardDir(unittest.TestCase):
    def test_with_dir(self) -> None:
        path = os.path.dirname(__file__)
        guard_dir(path)
        self.assertTrue(True)

    def test_with_file(self) -> None:
        path = __file__
        with pytest.raises(FileNotFoundError):
            guard_dir(path)

    def test_with_unknown_path(self) -> None:
        path = f"/tmp/{uuid.uuid4()}"
        with pytest.raises(FileNotFoundError):
            guard_dir(path)


class TestGuardPath(unittest.TestCase):
    def test_with_dir(self) -> None:
        path = os.path.dirname(__file__)
        with pytest.raises(FileNotFoundError):
            guard_path(path)

    def test_with_file(self) -> None:
        path = __file__
        guard_path(path)
        self.assertTrue(True)

    def test_with_unknown_path(self) -> None:
        path = f"/tmp/{uuid.uuid4()}"
        with pytest.raises(FileNotFoundError):
            guard_path(path)


class TestGuardUTCDatetime(unittest.TestCase):
    def test_with_utc(self) -> None:
        dt = datetime.now(tz=timezone.utc)
        guard_utc_datetime(dt)
        self.assertTrue(True)

    def test_without_utc(self) -> None:
        dt = datetime.now()
        with pytest.raises(ValueError):
            guard_utc_datetime(dt)
