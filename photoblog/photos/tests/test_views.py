import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, reverse_lazy
from PIL import Image

from photoblog.photos.models import Photo, Tag
from photoblog.photos.tests.factories import PhotoFactory, TagFactory


def _make_image():
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(buf, format="PNG")
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
    url = reverse_lazy("photos:photo_create")

    def test_get(self, client, auth_user):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.context["cancel_url"] == reverse("photos:photo_list")

    def test_htmx_partial(self, client, auth_user):
        response = client.get(
            self.url,
            headers={"HX-Request": "true", "HX-Target": "photo-form"},
        )
        assert response.status_code == 200

    def test_post_invalid(self, client, auth_user):
        response = client.post(self.url, data={})
        assert response.status_code == 200

    def test_post_valid(self, client, auth_user):
        response = client.post(
            self.url,
            data={"title": "My Photo", "image": _make_image()},
        )
        photo = Photo.objects.get()
        assert response.url == photo.get_absolute_url()

    def test_post_valid_creates_tags(self, client, auth_user):
        client.post(
            self.url,
            data={"title": "My Photo", "image": _make_image(), "tags": "nature travel"},
        )
        assert Tag.objects.filter(tag="nature").exists()
        assert Tag.objects.filter(tag="travel").exists()

    def test_post_valid_lowercases_tags(self, client, auth_user):
        client.post(
            self.url,
            data={"title": "My Photo", "image": _make_image(), "tags": "Nature"},
        )
        assert Tag.objects.filter(tag="nature").exists()

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("photos:photo_create"))
        assert response.url.startswith(reverse("account_login"))


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
        photo_url = photo.get_absolute_url()
        response = client.post(
            reverse("photos:photo_edit", args=[photo.pk]),
            data={"title": "Updated", "image": _make_image()},
        )
        assert response.url == photo_url

    def test_post_valid_saves_tags(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        client.post(
            reverse("photos:photo_edit", args=[photo.pk]),
            data={"title": "Updated", "image": _make_image(), "tags": "nature"},
        )
        assert list(photo.get_tags()) == ["nature"]

    def test_post_valid_replaces_existing_tags(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        tag = TagFactory(tag="old")
        photo.tags.add(tag)
        client.post(
            reverse("photos:photo_edit", args=[photo.pk]),
            data={"title": "Updated", "image": _make_image(), "tags": "new"},
        )
        assert list(photo.get_tags()) == ["new"]

    def test_get_populates_tags_initial(self, client, auth_user):
        photo = PhotoFactory(user=auth_user)
        tag = TagFactory(tag="nature")
        photo.tags.add(tag)
        response = client.get(reverse("photos:photo_edit", args=[photo.pk]))
        assert response.context["form"].fields["tags"].initial == "nature"

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


@pytest.mark.django_db
class TestTagDetail:
    def test_get(self, client, auth_user):
        TagFactory(tag="nature")
        response = client.get(reverse("photos:tag_detail", args=["nature"]))
        assert response.status_code == 200

    def test_htmx_partial(self, client, auth_user):
        TagFactory(tag="nature")
        response = client.get(
            reverse("photos:tag_detail", args=["nature"]),
            headers={"HX-Request": "true", "HX-Target": "pagination"},
        )
        assert response.status_code == 200

    def test_404(self, client, auth_user):
        response = client.get(reverse("photos:tag_detail", args=["nonexistent"]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client):
        TagFactory(tag="nature")
        response = client.get(reverse("photos:tag_detail", args=["nature"]))
        assert response.status_code == 302
