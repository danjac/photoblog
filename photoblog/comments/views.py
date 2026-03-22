from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from photoblog.comments.forms import CommentForm
from photoblog.comments.models import Comment
from photoblog.http.decorators import require_DELETE, require_form_methods
from photoblog.photos.models import Photo

if TYPE_CHECKING:
    from photoblog.http.request import HttpRequest
    from photoblog.http.response import RenderOrRedirectResponse


@login_required
@require_form_methods
def comment_create(request: HttpRequest, photo_id: int) -> RenderOrRedirectResponse:
    """Create a comment on a photo."""
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            messages.success(request, _("Comment added."))
            return redirect(photo)
    return redirect(photo)


@login_required
@require_form_methods
def comment_edit(request: HttpRequest, pk: int) -> RenderOrRedirectResponse:
    """Edit a comment."""
    comment = get_object_or_404(Comment.objects.select_related("photo"), pk=pk)
    if not request.user.has_perm("comments.change_comment", comment):
        raise PermissionDenied
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, _("Comment updated."))
            return redirect(comment.photo)
    else:
        form = CommentForm(instance=comment)
    return TemplateResponse(
        request,
        "comments/comment_form.html",
        {"form": form, "comment": comment},
    )


@login_required
@require_DELETE
def comment_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a comment."""
    comment = get_object_or_404(Comment, pk=pk)
    if not request.user.has_perm("comments.delete_comment", comment):
        raise PermissionDenied
    comment.delete()
    messages.success(request, _("Comment deleted."))
    return HttpResponse()
