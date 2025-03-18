import os
from pathlib import Path

import pytest

from source.classes.base_storage_manager import BaseStorageManager
from source.classes.db_manager import DBManager


def test_instance_success():
    db_filepath = Path('testing.db')
    dbm = DBManager(filepath=db_filepath)
    dbm.destroy()
    assert db_filepath.exists()
    os.remove(db_filepath)


@pytest.fixture
async def new_instance() -> DBManager:
    dbmanager = DBManager()
    yield dbmanager


def test_interface_success(new_instance: DBManager):
    assert isinstance(new_instance, BaseStorageManager)
