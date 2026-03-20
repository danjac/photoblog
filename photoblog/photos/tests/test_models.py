import pytest

from photoblog.photos.tests.factories import PhotoFactory


@pytest.mark.django_db
class TestPhoto:
    def test_create(self):
        obj = PhotoFactory()
        assert obj.pk is not None

    def test_str(self):
        obj = PhotoFactory()
        assert str(obj) == obj.title
