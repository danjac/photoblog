import pytest

from photoblog.photos.models import Photo
from photoblog.photos.tests.factories import PhotoFactory


@pytest.mark.django_db
class TestPhoto:
    def test_create(self):
        obj = PhotoFactory()
        assert obj.pk is not None

    def test_str(self):
        obj = PhotoFactory()
        assert str(obj) == obj.title


@pytest.mark.django_db
class TestPhotoSearch:
    def test_empty_value_returns_nothing(self):
        PhotoFactory(title="visible photo")
        assert list(Photo.objects.search("")) == []

    def test_matching_title_returned(self):
        photo = PhotoFactory(title="uniqueword")
        assert photo in Photo.objects.search("uniqueword")

    def test_matching_description_returned(self):
        photo = PhotoFactory(title="other", description="specificterm")
        assert photo in Photo.objects.search("specificterm")

    def test_non_matching_record_excluded(self):
        PhotoFactory(title="something else", description="unrelated")
        assert list(Photo.objects.search("uniqueword")) == []

    def test_search_annotates_rank(self):
        PhotoFactory(title="rankme")
        assert hasattr(Photo.objects.search("rankme").first(), "rank")

    def test_custom_annotation_name(self):
        PhotoFactory(title="annotated")
        assert hasattr(
            Photo.objects.search("annotated", annotation="score").first(), "score"
        )
