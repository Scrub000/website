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


from typing import Optional, Union

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.comments import models as comment_models
from website.domain import exceptions


def get_comment(id: Optional[int] = None) -> comment_models.Comment:
    """
    Determine whether a Comment is available via the provided keyword
    arguments.

    Raises:
        - `DoesNotExist` if the Comment does not exist.
    Returns:
        - The Comment associated to the provided `id`.
    """
    filters = []

    if id:
        filters.append(comment_models.Comment.id == id)
    comment = comment_models.Comment.query.filter(*filters).first()

    if not comment:
        raise exceptions.DoesNotExist("Comment does not exist.")
    return comment


def get_comments(
    author: Optional[Union[account_models.Account, int]] = None,
    blog: Optional[blog_models.Blog] = None,
    parent: Optional[comment_models.Comment] = None,
):
    """
    Get all comments matching the provided keyword arguments.

    Args:
        author (Account): Only comments associated with this author will be
        returned. To get comments with no author, use `0`.
        blog (Blog): Only comments asscoated with this blog will be returned.
        parent (Parent): Only comments asscoated with this parent will be
        returned.

    Returns:
        list: A list of comments.
    """
    filters = list()

    if author is not None and author != 0:
        filters.append(comment_models.Comment.author == author)
    if author == 0:
        filters.append(comment_models.Comment.author is None)
    if blog is not None:
        filters.append(comment_models.Comment.blog == blog)
    if parent is not None:
        filters.append(comment_models.Comment.parent == parent)

    comments = (
        comment_models.Comment.query.filter(*filters)
        .order_by(
            comment_models.Comment.thread_at.desc(),
            comment_models.Comment.path.asc(),
        )
        .all()
    )

    return comments
