from typing import ClassVar

from django import forms

from photoblog.photos.models import Photo
from photoblog.photos.widgets import ThumbnailWidget


class PhotoForm(forms.ModelForm):
    """Form for creating and editing Photo instances."""

    class Meta:
        model = Photo
        fields = (
            "title",
            "image",
            "description",
        )
        widgets: ClassVar[dict] = {"image": ThumbnailWidget}
