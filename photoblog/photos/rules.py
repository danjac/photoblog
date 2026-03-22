import rules  # type: ignore[reportMissingTypeStubs]


@rules.predicate  # type: ignore[reportPrivateImportUsage]
def is_photo_owner(user, photo):
    """Return True if the user owns the photo."""
    return photo.user_id == user.pk


rules.add_perm("photos.change_photo", is_photo_owner)  # type: ignore[reportPrivateImportUsage]
rules.add_perm("photos.delete_photo", is_photo_owner)  # type: ignore[reportPrivateImportUsage]
