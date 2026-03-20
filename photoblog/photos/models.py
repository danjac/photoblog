import sorl.thumbnail
from django.conf import settings
from django.db import models


class Photo(models.Model):
    """A user-uploaded photo."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = sorl.thumbnail.ImageField(upload_to="photos/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the photo's title."""
        return self.title
