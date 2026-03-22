import pytest

from photoblog.comments.rules import is_comment_owner
from photoblog.comments.tests.factories import CommentFactory
from photoblog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestIsCommentOwner:
    def test_owner_allowed(self):
        """Comment owner passes the predicate."""
        comment = CommentFactory()
        assert is_comment_owner(comment.user, comment)

    def test_non_owner_denied(self):
        """A different user fails the predicate."""
        comment = CommentFactory()
        other = UserFactory()
        assert not is_comment_owner(other, comment)

    def test_has_perm_change(self):
        """Owner has the change_comment permission."""
        comment = CommentFactory()
        assert comment.user.has_perm("comments.change_comment", comment)

    def test_has_perm_delete(self):
        """Owner has the delete_comment permission."""
        comment = CommentFactory()
        assert comment.user.has_perm("comments.delete_comment", comment)

    def test_no_perm_change_other_user(self):
        """Non-owner does not have the change_comment permission."""
        comment = CommentFactory()
        other = UserFactory()
        assert not other.has_perm("comments.change_comment", comment)

    def test_no_perm_delete_other_user(self):
        """Non-owner does not have the delete_comment permission."""
        comment = CommentFactory()
        other = UserFactory()
        assert not other.has_perm("comments.delete_comment", comment)
