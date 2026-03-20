import pytest

from photoblog.comments.tests.factories import CommentFactory


@pytest.fixture
def comment() -> CommentFactory:
    return CommentFactory()
