from typing import ClassVar

from django.forms.widgets import FileInput, TextInput


class ThumbnailWidget(FileInput):
    """File input widget that renders a sorl thumbnail preview in forms/partials.html."""


class TagWidget(TextInput):
    """Text input that renders as an Alpine.js pill/chip tag editor in forms/partials.html."""

    class Media:
        js: ClassVar = ("photos/tags.js",)
