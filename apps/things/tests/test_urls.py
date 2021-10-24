import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_thing_list_reverse():
    expected_url = '/things/'
    reversed_url = reverse('things:list')
    assert expected_url == reversed_url
