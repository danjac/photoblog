from django.contrib import admin

from photoblog.photos.models import Photo, Tag


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin for Photo model."""

    list_display = ("title", "user", "created")
    search_fields = ("title", "description")
    list_filter = ()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag model."""

    list_display = ("tag",)
    search_fields = ("tag",)
    list_filter = ()
