#   Website
#   Copyright © 2019-2020  scrub
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.comments import models as comment_models
from website.domain import exceptions


def create_comment(
    body: str,
    author: account_models.Account,
    blog: Optional[blog_models.Blog] = None,
    parent: Optional[comment_models.Comment] = None,
) -> comment_models.Comment:
    """
    Create a Comment in the database.

    Raises:
        - `UnableToCreate` if Comment cannot be created.

    Returns:
        - A new Comment.
    """
    if not blog and not parent:
        raise exceptions.UnableToCreate(
            "A blog or a parent comment must be provided"
        )
    if author.is_anonymous or not author.is_confirmed:
        raise exceptions.UnableToCreate(
            "Unable to comment without a confirmed account"
        )

    if blog:
        if not blog.comment:
            raise exceptions.UnableToCreate(
                "Cannot create comments on this blog"
            )
        thread_at = None
    elif parent:
        blog = parent.blog
        thread_at = parent.thread_at

    try:
        comment = comment_models.Comment.new(
            body=body,
            author=author,
            blog=blog,
            parent=parent,
            thread_at=thread_at,
        )
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToCreate("Unable to create comment")

    # TODO: Publish an event

    return comment


def update_comment(comment: comment_models.Comment, **kwargs):
    """
    Update a Comment in the database.

    Raises:
        - `UnableToUpdate` if Comment cannot be updated.
    """
    try:
        comment.update(**kwargs)
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToUpdate("Unable to update comment.")

    # TODO: Publish an event


def delete_comment(comment: comment_models.Comment):
    """
    Delete a Comment from the database.
    """
    try:
        comment.delete()
    except Exception:
        raise exceptions.UnableToDelete("Unable to delete comment.")

    # TODO: Send comms emails

    # TODO: Publish an event
