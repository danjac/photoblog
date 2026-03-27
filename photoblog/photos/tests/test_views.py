import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image as PilImage

from photoblog.photos.tests.factories import PhotoFactory


def _make_image():
    buf = io.BytesIO()
    PilImage.new("RGB", (10, 10), color="blue").save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile("test.png", buf.read(), content_type="image/png")


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

    def test_search(self, client, auth_user):
        PhotoFactory(title="uniqueword")
        response = client.get(reverse("photos:photo_list"), {"search": "uniqueword"})
        assert response.status_code == 200

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("photos:photo_list"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestUserPhotoList:
    def test_get(self, client, auth_user):
        PhotoFactory(user=auth_user)
        response = client.get(
            reverse("photos:user_photo_list", args=[auth_user.username])
        )
        assert response.status_code == 200

    def test_404(self, client, auth_user):
        response = client.get(reverse("photos:user_photo_list", args=["nobody"]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client, photo):
        response = client.get(
            reverse("photos:user_photo_list", args=[photo.user.username])
        )
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
        assert response.context["cancel_url"] == reverse("photos:photo_list")

    def test_htmx_partial(self, client, auth_user):
        response = client.get(
            reverse("photos:photo_create"),
            headers={"HX-Request": "true", "HX-Target": "photo-form"},
        )
        assert response.status_code == 200

    def test_post_invalid(self, client, auth_user):
        response = client.post(reverse("photos:photo_create"), data={})
        assert response.status_code == 200

    def test_post_valid(self, client, auth_user):
        response = client.post(
            reverse("photos:photo_create"),
            data={"title": "My Photo", "image": _make_image()},
        )
        assert response.status_code == 302

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("photos:photo_create"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestPhotoEdit:
    def test_get(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        photo_url = photo.get_absolute_url()
        response = client.get(photo_url)
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

    def test_post_valid(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        response = client.post(
            reverse("photos:photo_edit", args=[photo.pk]),
            data={"title": "Updated", "image": _make_image()},
        )
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
        response = client.post(reverse("photos:photo_delete", args=[pk]))
        assert response.status_code == 302
        assert not PhotoFactory._meta.model.objects.filter(pk=pk).exists()

    def test_404(self, client, auth_user):
        response = client.post(reverse("photos:photo_delete", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client, photo):
        response = client.get(reverse("photos:photo_delete", args=[photo.pk]))
        assert response.status_code == 302

    def test_permission_denied_if_not_owner(self, client, auth_user, other_user_photo):
        response = client.get(
            reverse("photos:photo_delete", args=[other_user_photo.pk])
        )
        assert response.status_code == 403
