import pytest

from photoblog.photos.forms import PhotoForm
from photoblog.photos.models import Tag
from photoblog.photos.tests.factories import PhotoFactory, TagFactory


class TestPhotoFormCleanTags:
    def test_valid_slug_tags_pass(self):
        form = PhotoForm(data={"title": "x", "tags": "nature travel"})
        form.full_clean()
        assert "tags" not in form.errors

    def test_invalid_tag_raises_error(self):
        form = PhotoForm(data={"title": "x", "tags": "hello world!"})
        form.full_clean()
        assert "tags" in form.errors

    def test_empty_tags_pass(self):
        form = PhotoForm(data={"title": "x", "tags": ""})
        form.full_clean()
        assert "tags" not in form.errors

    def test_tags_are_lowercased_before_validation(self):
        form = PhotoForm(data={"title": "x", "tags": "Nature"})
        form.full_clean()
        assert "tags" not in form.errors


@pytest.mark.django_db
class TestPhotoFormSaveTags:
    def test_creates_new_tags(self):
        photo = PhotoFactory()
        form = PhotoForm(data={"title": "x", "tags": "nature travel"})
        form.full_clean()
        form.save_tags(photo)
        assert set(photo.get_tags()) == {"nature", "travel"}

    def test_lowercases_tags_on_save(self):
        photo = PhotoFactory()
        form = PhotoForm(data={"title": "x", "tags": "Nature"})
        form.full_clean()
        form.save_tags(photo)
        assert list(photo.get_tags()) == ["nature"]

    def test_replaces_existing_tags(self):
        photo = PhotoFactory()
        photo.tags.add(TagFactory(tag="old"))
        form = PhotoForm(data={"title": "x", "tags": "new"})
        form.full_clean()
        form.save_tags(photo)
        assert list(photo.get_tags()) == ["new"]

    def test_clears_tags_when_empty(self):
        photo = PhotoFactory()
        photo.tags.add(TagFactory(tag="old"))
        form = PhotoForm(data={"title": "x", "tags": ""})
        form.full_clean()
        form.save_tags(photo)
        assert list(photo.get_tags()) == []

    def test_reuses_existing_tag_objects(self):
        photo = PhotoFactory()
        TagFactory(tag="nature")
        form = PhotoForm(data={"title": "x", "tags": "nature"})
        form.full_clean()
        form.save_tags(photo)
        assert Tag.objects.filter(tag="nature").count() == 1
