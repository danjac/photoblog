from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csp import csp_override
from django.views.decorators.http import require_safe

from photoblog.comments.forms import CommentForm
from photoblog.comments.models import Comment
from photoblog.http.decorators import require_form_methods
from photoblog.paginator import PaginationConfig, render_paginated_response
from photoblog.partials import render_partial_response
from photoblog.photos.forms import PhotoForm
from photoblog.photos.models import Photo
from photoblog.users.models import User

if TYPE_CHECKING:
    from photoblog.http.request import HttpRequest
    from photoblog.http.response import RenderOrRedirectResponse


@require_safe
@login_required
def user_photo_list(request: HttpRequest, username: str) -> TemplateResponse:
    """Display a paginated list of photos by a specific user."""
    user = get_object_or_404(User, username=username, is_active=True)
    return render_paginated_response(
        request,
        "photos/user_photo_list.html",
        Photo.objects.filter(user=user)
        .only("pk", "title", "image")
        .order_by("-created"),
        extra_context={"submitter": user},
    )


@require_safe
@login_required
def photo_list(request: HttpRequest) -> TemplateResponse:
    """Display a paginated list of all photos."""
    photos = Photo.objects.only("pk", "title", "image")
    if request.search:
        photos = photos.search(request.search.value).order_by("-rank", "-created")
    else:
        photos = photos.order_by("-created")
    return render_paginated_response(request, "photos/photo_list.html", photos)


@require_safe
@login_required
def photo_detail(request: HttpRequest, pk: int) -> TemplateResponse:
    """Display a single photo."""
    photo = get_object_or_404(Photo.objects.select_related("user"), pk=pk)
    comment_form = CommentForm() if request.user.is_authenticated else None
    comments = (
        Comment.objects.filter(photo=photo).select_related("user").order_by("-created")
    )
    return render_paginated_response(
        request,
        "photos/photo_detail.html",
        comments,
        extra_context={"photo": photo, "comment_form": comment_form},
        config=PaginationConfig(target="comment-list", partial="comment-list"),
    )


@csp_override(settings.SECURE_CSP_UPLOAD)
@login_required
@require_form_methods
def photo_create(request: HttpRequest) -> RenderOrRedirectResponse:
    """Create a new photo."""
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, _("Photo created."))
            return redirect("photos:photo_list")
    else:
        form = PhotoForm()
    return render_partial_response(
        request,
        "photos/photo_form.html",
        {
            "form": form,
            "cancel_url": reverse("photos:photo_list"),
        },
        target="photo-form",
        partial="photo-form",
    )


@csp_override(settings.SECURE_CSP_UPLOAD)
@login_required
@require_form_methods
def photo_edit(request: HttpRequest, pk: int) -> RenderOrRedirectResponse:
    """Edit an existing photo."""
    photo = get_object_or_404(Photo, pk=pk)
    if not request.user.has_perm("photos.change_photo", photo):
        raise PermissionDenied
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, _("Photo updated."))
            return redirect(photo)
    else:
        form = PhotoForm(instance=photo)
    return render_partial_response(
        request,
        "photos/photo_form.html",
        {
            "form": form,
            "photo": photo,
            "cancel_url": photo.get_absolute_url(),
        },
        target="photo-form",
        partial="photo-form",
    )


@login_required
@require_form_methods
def photo_delete(request: HttpRequest, pk: int) -> RenderOrRedirectResponse:
    """Delete a photo."""
    photo = get_object_or_404(Photo, pk=pk)
    if not request.user.has_perm("photos.delete_photo", photo):
        raise PermissionDenied
    if request.method == "POST":
        photo.delete()
        messages.success(request, _("Photo deleted."))
        return redirect(reverse("photos:photo_list"))
    return TemplateResponse(
        request,
        "photos/photo_confirm_delete.html",
        {"photo": photo},
    )
