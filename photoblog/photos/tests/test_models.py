import pytest
from django.db import IntegrityError

from photoblog.photos.models import Photo, upload_handler
from photoblog.photos.tests.factories import PhotoFactory, TagFactory


class TestUploadHandler:
    def test_extension_preserved(self):
        assert upload_handler(None, "photo.jpg").endswith(".jpg")

    def test_extension_lowercased(self):
        assert upload_handler(None, "photo.JPG").endswith(".jpg")

    def test_stored_under_photos_dir(self):
        assert upload_handler(None, "photo.jpg").startswith("photos/")

    def test_unique_per_call(self):
        assert upload_handler(None, "photo.jpg") != upload_handler(None, "photo.jpg")

    def test_original_name_discarded(self):
        path = upload_handler(None, "my_holiday.jpg")
        assert "my_holiday" not in path


@pytest.mark.django_db
class TestPhoto:
    def test_create(self):
        obj = PhotoFactory()
        assert obj.pk is not None

    def test_str(self):
        obj = PhotoFactory()
        assert str(obj) == obj.title

    def test_get_tags_returns_tag_names(self):
        photo = PhotoFactory()
        tag = TagFactory(tag="nature")
        photo.tags.add(tag)
        assert list(photo.get_tags()) == ["nature"]

    def test_get_tags_empty(self):
        photo = PhotoFactory()
        assert list(photo.get_tags()) == []


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


@pytest.mark.django_db
class TestTag:
    def test_create(self):
        obj = TagFactory()
        assert obj.pk is not None

    def test_str(self):
        obj = TagFactory(tag="nature")
        assert str(obj) == "nature"

    def test_tag_unique(self):
        TagFactory(tag="duplicate")
        with pytest.raises(IntegrityError):
            TagFactory(tag="duplicate")
