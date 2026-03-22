from django.forms.widgets import FileInput


class ThumbnailWidget(FileInput):
    """File input widget that renders a sorl thumbnail preview in forms/partials.html."""
