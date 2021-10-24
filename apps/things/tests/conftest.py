import pytest

from .factories import ThingFactory


@pytest.fixture()
def thing():
    return ThingFactory()
