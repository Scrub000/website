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

from typing import List, Optional

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.domain import exceptions, utils


def create_blog(
    title: str,
    body: str,
    author: account_models.Account,
    description: Optional[str] = None,
    categories: Optional[List[category_models.Category]] = None,
    published: bool = False,
    comment: bool = False,
) -> blog_models.Blog:
    """
    Create a Blog in the database.

    Raises:
        - `UnableToCreate` if Blog cannot be created.
    Returns:
        - A new Blog.
    """
    # TODO: This is a race condition (slug is unique when called, but possibly
    # not when new() is called). We need to lock the blogs table to ensure that
    # the slug is actually unique.
    try:
        slug = utils.unique_slugify(
            model=blog_models.Blog, text=title, max_length=200
        )
    except exceptions.UnableToGenerateSlug:
        # TODO: Publish an event
        raise exceptions.UnableToCreate("Unable to create blog.")
    try:
        blog = blog_models.Blog.new(
            title=title,
            slug=slug,
            body=body,
            author=author,
            description=description,
            categories=categories,
            published=published,
            comment=comment,
        )
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToCreate("Unable to create blog.")

    # TODO: Publish an event

    return blog


def update_blog(blog: blog_models.Blog, **kwargs):
    """
    Update a Blog in the database.

    Raises:
        - `UnableToUpdate` if Blog cannot be updated.
    """
    try:
        blog.update(**kwargs)
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToUpdate("Unable to update blog.")

    # TODO: Publish an event


def delete_blog(blog: blog_models.Blog):
    """
    Delete a Blog from the database.
    """
    try:
        blog.delete()
    except Exception:
        raise exceptions.UnableToDelete("Unable to delete blog.")

    # TODO: Send comms emails

    # TODO: Publish an event
