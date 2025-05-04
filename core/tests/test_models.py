import pytest
from core.models import Item

@pytest.mark.django_db
def test_item_crud():
    apple = Item.objects.create(name="Apple")
    fetched = Item.objects.get(name="Apple")
    assert fetched == apple