from typing import Callable

import pytest

from source.classes.base_storage_manager import BaseStorageManager


class FullSample(BaseStorageManager):
    #  Methods
    store: Callable = lambda: ()
    retrieve: Callable = lambda: ()


def test_instance_success():
    assert isinstance(FullSample(), BaseStorageManager)


class EmptySample(BaseStorageManager):
    pass


def test_instance_failure():
    with pytest.raises(TypeError):
        EmptySample()
