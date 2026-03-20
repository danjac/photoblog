import pytest
from django.urls import reverse

from photoblog.comments.tests.factories import CommentFactory
from photoblog.photos.tests.factories import PhotoFactory


@pytest.mark.django_db
class TestCommentCreate:
    def test_post_valid(self, client, auth_user):
        photo = PhotoFactory()
        response = client.post(
            reverse("comments:comment_create", args=[photo.pk]),
            data={"comment": "Great photo!"},
        )
        assert response.status_code == 302
        assert photo.comments.filter(user=auth_user).exists()

    def test_post_invalid(self, client, auth_user):
        photo = PhotoFactory()
        response = client.post(
            reverse("comments:comment_create", args=[photo.pk]),
            data={"comment": ""},
        )
        assert response.status_code == 302

    def test_404(self, client, auth_user):
        response = client.post(
            reverse("comments:comment_create", args=[0]),
            data={"comment": "Great photo!"},
        )
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client):
        photo = PhotoFactory()
        response = client.post(
            reverse("comments:comment_create", args=[photo.pk]),
            data={"comment": "Great photo!"},
        )
        assert response.status_code == 302


@pytest.mark.django_db
class TestCommentEdit:
    def test_get(self, client, auth_user):
        comment = CommentFactory(user=auth_user)
        response = client.get(reverse("comments:comment_edit", args=[comment.pk]))
        assert response.status_code == 200

    def test_post_valid(self, client, auth_user):
        comment = CommentFactory(user=auth_user)
        response = client.post(
            reverse("comments:comment_edit", args=[comment.pk]),
            data={"comment": "Updated comment."},
        )
        assert response.status_code == 302
        comment.refresh_from_db()
        assert comment.comment == "Updated comment."

    def test_post_invalid(self, client, auth_user):
        comment = CommentFactory(user=auth_user)
        response = client.post(
            reverse("comments:comment_edit", args=[comment.pk]),
            data={"comment": ""},
        )
        assert response.status_code == 200

    def test_404(self, client, auth_user):
        response = client.get(reverse("comments:comment_edit", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client):
        comment = CommentFactory()
        response = client.get(reverse("comments:comment_edit", args=[comment.pk]))
        assert response.status_code == 302

    def test_permission_denied_if_not_owner(self, client, auth_user):
        comment = CommentFactory()
        response = client.get(reverse("comments:comment_edit", args=[comment.pk]))
        assert response.status_code == 403


@pytest.mark.django_db
class TestCommentDelete:
    def test_delete(self, client, auth_user):
        comment = CommentFactory(user=auth_user)
        pk = comment.pk
        response = client.delete(reverse("comments:comment_delete", args=[pk]))
        assert response.status_code == 200
        assert not CommentFactory._meta.model.objects.filter(pk=pk).exists()

    def test_404(self, client, auth_user):
        response = client.delete(reverse("comments:comment_delete", args=[0]))
        assert response.status_code == 404

    def test_redirect_if_not_logged_in(self, client):
        comment = CommentFactory()
        response = client.delete(reverse("comments:comment_delete", args=[comment.pk]))
        assert response.status_code == 302

    def test_permission_denied_if_not_owner(self, client, auth_user):
        comment = CommentFactory()
        response = client.delete(reverse("comments:comment_delete", args=[comment.pk]))
        assert response.status_code == 403
