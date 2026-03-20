from typing import ClassVar

from django.contrib import admin

from photoblog.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin for Photo model."""

    list_display: ClassVar[list[str]] = ["title", "user", "created"]
    search_fields: ClassVar[list[str]] = ["title", "description"]
    list_filter: ClassVar[list[str]] = []
