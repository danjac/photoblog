from typing import ClassVar

from django import forms
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _

from photoblog.photos.models import Photo, Tag
from photoblog.photos.widgets import TagWidget, ThumbnailWidget


class PhotoForm(forms.ModelForm):
    """Form for creating and editing Photo instances."""

    tags = forms.CharField(
        required=False,
        label=_("Tags"),
        help_text=_("Space-separated list of tags"),
        widget=TagWidget(),
    )

    field_order = ("title", "image", "tags", "description")

    class Meta:
        model = Photo
        fields = (
            "title",
            "image",
            "description",
        )
        widgets: ClassVar[dict] = {"image": ThumbnailWidget}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tags"].initial = " ".join(self.instance.get_tags())

    def clean_tags(self) -> str:
        """Validate that each tag is a valid slug."""
        value = self.cleaned_data["tags"]
        for tag in value.split():
            validate_slug(tag.lower())
        return value

    def save_tags(self, photo: Photo) -> None:
        """Split, lowercase, bulk-create and assign tags to the photo."""
        tag_values = [t.lower() for t in self.cleaned_data["tags"].split() if t]
        Tag.objects.bulk_create(
            [Tag(tag=t) for t in tag_values],
            ignore_conflicts=True,
        )
        photo.tags.set(Tag.objects.filter(tag__in=tag_values))  # type: ignore[attr-defined]
