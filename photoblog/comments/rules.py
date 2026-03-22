import rules  # type: ignore[reportMissingTypeStubs]


@rules.predicate  # type: ignore[reportPrivateImportUsage]
def is_comment_owner(user, comment):
    """Return True if the user owns the comment."""
    return comment.user_id == user.pk


rules.add_perm("comments.change_comment", is_comment_owner)  # type: ignore[reportPrivateImportUsage]
rules.add_perm("comments.delete_comment", is_comment_owner)  # type: ignore[reportPrivateImportUsage]
