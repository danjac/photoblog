from typing import TYPE_CHECKING

from django.urls import path

from photoblog.comments import views

if TYPE_CHECKING:
    from django.urls import URLPattern, URLResolver

app_name = "comments"
urlpatterns: list[URLPattern | URLResolver] = [
    path("photo/<int:photo_id>/comment/", views.comment_create, name="comment_create"),
    path("comment/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
