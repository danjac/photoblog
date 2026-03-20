import sorl.thumbnail
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse


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

    def get_absolute_url(self) -> str:
        """Return the URL for this photo."""
        return reverse("photos:photo_detail", kwargs={"pk": self.pk})


@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    """Delete the image file from storage when a Photo is deleted."""
    instance.image.delete(save=False)
