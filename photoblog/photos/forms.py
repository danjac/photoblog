from typing import ClassVar

from django import forms

from photoblog.photos.models import Photo


class PhotoForm(forms.ModelForm):
    """Form for creating and editing Photo instances."""

    class Meta:
        model = Photo
        fields: ClassVar[list[str]] = ["title", "description", "image"]
