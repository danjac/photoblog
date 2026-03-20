from typing import ClassVar

from django.contrib import admin

from photoblog.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model."""

    list_display: ClassVar[list[str]] = ["user", "photo", "created"]
    search_fields: ClassVar[list[str]] = ["comment"]
    list_filter: ClassVar[list[str]] = []
