from django.conf import settings
from django.db import models

from photoblog.photos.models import Photo


class Comment(models.Model):
    """A comment on a photo."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        """Return first 50 chars of comment."""
        return self.comment[:50]
