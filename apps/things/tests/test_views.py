import pytest

from ..views import ThingRetrieve


@pytest.mark.django_db
def test_get_object(thing):
    view = ThingRetrieve(kwargs={'pk': thing.pk})
    assert view.get_object() == thing
