import pytest

from source.classes.website_handler import WebsiteHandler


@pytest.fixture
def new_instance() -> WebsiteHandler:
    return WebsiteHandler()


def test_instantiation_success(new_instance: WebsiteHandler):
    assert isinstance(new_instance, WebsiteHandler)
