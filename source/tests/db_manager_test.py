import pytest

from source.classes.base_storage_manager import BaseStorageManager
from source.classes.db_manager import DBManager


@pytest.fixture
async def new_instance() -> DBManager:
    dbmanager = DBManager()
    yield dbmanager


def test_interface_success(new_instance: DBManager):
    assert isinstance(new_instance, BaseStorageManager)
