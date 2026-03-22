import pytest

from photoblog.photos.rules import is_photo_owner
from photoblog.photos.tests.factories import PhotoFactory
from photoblog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestIsPhotoOwner:
    def test_owner_allowed(self):
        """Photo owner passes the predicate."""
        photo = PhotoFactory()
        assert is_photo_owner(photo.user, photo)

    def test_non_owner_denied(self):
        """A different user fails the predicate."""
        photo = PhotoFactory()
        other = UserFactory()
        assert not is_photo_owner(other, photo)

    def test_has_perm_change(self):
        """Owner has the change_photo permission."""
        photo = PhotoFactory()
        assert photo.user.has_perm("photos.change_photo", photo)

    def test_has_perm_delete(self):
        """Owner has the delete_photo permission."""
        photo = PhotoFactory()
        assert photo.user.has_perm("photos.delete_photo", photo)

    def test_no_perm_change_other_user(self):
        """Non-owner does not have the change_photo permission."""
        photo = PhotoFactory()
        other = UserFactory()
        assert not other.has_perm("photos.change_photo", photo)

    def test_no_perm_delete_other_user(self):
        """Non-owner does not have the delete_photo permission."""
        photo = PhotoFactory()
        other = UserFactory()
        assert not other.has_perm("photos.delete_photo", photo)
