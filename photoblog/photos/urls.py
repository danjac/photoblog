from typing import TYPE_CHECKING

from django.urls import path

from photoblog.photos import views

if TYPE_CHECKING:
    from django.urls import URLPattern, URLResolver

app_name = "photos"
urlpatterns: list[URLPattern | URLResolver] = [
    path("photos/", views.photo_list, name="photo_list"),
    path("photos/users/<str:username>/", views.user_photo_list, name="user_photo_list"),
    path("photos/create/", views.photo_create, name="photo_create"),
    path("photos/<int:pk>/", views.photo_detail, name="photo_detail"),
    path("photos/<int:pk>/edit/", views.photo_edit, name="photo_edit"),
    path("photos/<int:pk>/delete/", views.photo_delete, name="photo_delete"),
]
