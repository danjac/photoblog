from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "photoblog.comments"

    def ready(self):
        import photoblog.comments.rules  # noqa: F401
