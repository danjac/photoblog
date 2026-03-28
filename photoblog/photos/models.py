from typing import TYPE_CHECKING

import sorl.thumbnail
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from photoblog.db.search import Searchable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from django.db.models import Manager


class PhotoQuerySet(Searchable, models.QuerySet["Photo"]):
    """QuerySet for Photo with full-text search support."""

    default_search_fields = ("search_vector",)


class Photo(models.Model):
    """A user-uploaded photo."""

    if TYPE_CHECKING:
        tags: Manager[Tag]

    objects: PhotoQuerySet = PhotoQuerySet.as_manager()  # type: ignore[assignment]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    title = models.CharField(max_length=250, verbose_name=_("title"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    image = sorl.thumbnail.ImageField(upload_to="photos/", verbose_name=_("image"))
    search_vector = SearchVectorField(null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        """Return the photo's title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the URL for this photo."""
        return reverse("photos:photo_detail", kwargs={"pk": self.pk})

    def get_tags(self) -> Iterable[str]:
        """Return a flat iterable of tag name strings for this photo."""
        return self.tags.order_by("tag").values_list("tag", flat=True)


class Tag(models.Model):
    """A tag that can be applied to photos."""

    tag = models.SlugField(
        max_length=60, unique=True, blank=True, verbose_name=_("tag")
    )
    photos = models.ManyToManyField(
        "Photo",
        related_name="tags",
        blank=True,
        verbose_name=_("photos"),
    )

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self) -> str:
        """Return the tag value."""
        return self.tag


@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    """Delete the image file from storage when a Photo is deleted."""
    instance.image.delete(save=False)
