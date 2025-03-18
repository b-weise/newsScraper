import os
from pathlib import Path

import pytest
from pandas import DataFrame

from source.classes.base_storage_manager import BaseStorageManager
from source.classes.db_manager import DBManager
from source.interfaces.db_tables import MatchingArticles


def test_instance_success():
    db_filepath = Path('testing.db')
    dbm = DBManager(filepath=db_filepath)
    dbm.destroy()
    assert db_filepath.exists()
    os.remove(db_filepath)


@pytest.fixture
async def new_instance() -> DBManager:
    db_filepath = Path('testing.db')
    dbmanager = DBManager(filepath=db_filepath)
    yield dbmanager
    dbmanager.destroy()
    if db_filepath.exists():
        os.remove(db_filepath)


def test_interface_success(new_instance: DBManager):
    assert isinstance(new_instance, BaseStorageManager)


def test_retrieve_success(new_instance: DBManager):
    result = new_instance.retrieve(columns=[MatchingArticles.ID])
    assert isinstance(result, DataFrame)
