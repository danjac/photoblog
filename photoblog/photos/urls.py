from typing import TYPE_CHECKING

from django.urls import path

from photoblog.photos import views

if TYPE_CHECKING:
    from django.urls import URLPattern, URLResolver

app_name = "photos"
urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.photo_list, name="photo_list"),
    path("users/<str:username>/", views.user_photo_list, name="user_photo_list"),
    path("create/", views.photo_create, name="photo_create"),
    path("<int:pk>/", views.photo_detail, name="photo_detail"),
    path("<int:pk>/edit/", views.photo_edit, name="photo_edit"),
    path("<int:pk>/delete/", views.photo_delete, name="photo_delete"),
    path("tags/<slug:tag>/", views.tag_detail, name="tag_detail"),
]
