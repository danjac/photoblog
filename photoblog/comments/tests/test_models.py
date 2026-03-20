import pytest

from photoblog.comments.tests.factories import CommentFactory


@pytest.mark.django_db
class TestComment:
    def test_create(self):
        obj = CommentFactory()
        assert obj.pk is not None

    def test_str(self):
        obj = CommentFactory()
        assert str(obj) == obj.comment[:50]
