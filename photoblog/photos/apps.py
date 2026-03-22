from django.apps import AppConfig


class PhotosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "photoblog.photos"

    def ready(self):
        import photoblog.photos.rules  # noqa: F401
