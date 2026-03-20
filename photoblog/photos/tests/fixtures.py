import pytest

from photoblog.photos.tests.factories import PhotoFactory
from photoblog.users.tests.factories import UserFactory


@pytest.fixture
def photo() -> PhotoFactory:
    return PhotoFactory()


@pytest.fixture
def other_user_photo() -> PhotoFactory:
    return PhotoFactory(user=UserFactory())
