#   Website
#   Copyright © 2019-2020  Scrub
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

from ...data.accounts import models as account_models
from ...data.blogs import models as blog_models
from ...data.comments import models as comment_models
from ...domain import exceptions


def create_comment(
    body: str,
    author: account_models.Account,
    blog: blog_models.Blog,
    parent: comment_models.Comment = None,
) -> comment_models.Comment:
    """
    Create a Comment in the database.

    Raises:
        - `UnableToCreate` if Comment cannot be created.

    Returns:
        - A new Comment.
    """
    if author.is_anonymous or not author.is_confirmed:
        raise exceptions.UnableToCreate(
            "Unable to comment without a confirmed account"
        )
    if not blog.comment:
        raise exceptions.UnableToCreate("Cannot create comments on this blog")
    thread_at = None
    if parent:
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
