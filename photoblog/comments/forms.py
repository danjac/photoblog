from typing import ClassVar

from django import forms

from photoblog.comments.models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating a comment."""

    class Meta:
        model = Comment
        fields: ClassVar[list[str]] = ["comment"]
