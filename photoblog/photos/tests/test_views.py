import pytest
from django.urls import reverse

from photoblog.photos.tests.factories import PhotoFactory


@pytest.mark.django_db
class TestPhotoList:
    def test_get(self, client, auth_user):
        PhotoFactory.create_batch(3)
        response = client.get(reverse("photos:photo_list"))
        assert response.status_code == 200

    def test_htmx_partial(self, client, auth_user):
        response = client.get(
            reverse("photos:photo_list"),
            headers={"HX-Request": "true", "HX-Target": "photo-list"},
        )
        assert response.status_code == 200

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("photos:photo_list"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestPhotoDetail:
    def test_get(self, client, auth_user, photo):
        response = client.get(reverse("photos:photo_detail", args=[photo.pk]))
        assert response.status_code == 200

    def test_404(self, client, auth_user):
        response = client.get(reverse("photos:photo_detail", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client, photo):
        response = client.get(reverse("photos:photo_detail", args=[photo.pk]))
        assert response.status_code == 302


@pytest.mark.django_db
class TestPhotoCreate:
    def test_get(self, client, auth_user):
        response = client.get(reverse("photos:photo_create"))
        assert response.status_code == 200

    def test_htmx_partial(self, client, auth_user):
        response = client.get(
            reverse("photos:photo_create"),
            headers={"HX-Request": "true", "HX-Target": "photo-form"},
        )
        assert response.status_code == 200

    def test_post_invalid(self, client, auth_user):
        response = client.post(reverse("photos:photo_create"), data={})
        assert response.status_code == 200

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("photos:photo_create"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestPhotoEdit:
    def test_get(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        response = client.get(reverse("photos:photo_edit", args=[photo.pk]))
        assert response.status_code == 200

    def test_htmx_partial(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        response = client.get(
            reverse("photos:photo_edit", args=[photo.pk]),
            headers={"HX-Request": "true", "HX-Target": "photo-form"},
        )
        assert response.status_code == 200

    def test_post_invalid(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        response = client.post(
            reverse("photos:photo_edit", args=[photo.pk]),
            data={},
        )
        assert response.status_code == 200

    def test_404(self, client, auth_user):
        response = client.get(reverse("photos:photo_edit", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client, photo):
        response = client.get(reverse("photos:photo_edit", args=[photo.pk]))
        assert response.status_code == 302

    def test_permission_denied_if_not_owner(self, client, auth_user, other_user_photo):
        response = client.get(reverse("photos:photo_edit", args=[other_user_photo.pk]))
        assert response.status_code == 403


@pytest.mark.django_db
class TestPhotoDelete:
    def test_get(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        response = client.get(reverse("photos:photo_delete", args=[photo.pk]))
        assert response.status_code == 200

    def test_delete(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        pk = photo.pk
        response = client.delete(reverse("photos:photo_delete", args=[pk]))
        assert response.status_code == 302
        assert not PhotoFactory._meta.model.objects.filter(pk=pk).exists()

    def test_404(self, client, auth_user):
        response = client.delete(reverse("photos:photo_delete", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client, photo):
        response = client.get(reverse("photos:photo_delete", args=[photo.pk]))
        assert response.status_code == 302

    def test_permission_denied_if_not_owner(self, client, auth_user, other_user_photo):
        response = client.get(
            reverse("photos:photo_delete", args=[other_user_photo.pk])
        )
        assert response.status_code == 403
