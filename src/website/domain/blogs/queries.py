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


from ...data.blogs import models as blog_models
from ...data.categories import models as category_models
from .. import exceptions


def get_blog(slug: str = None) -> tuple:
    """
    Determine whether a Blog is available via the provided keyword arguments.

    Raises:
        - `DoesNotExist` if the Blog does not exist.
    Returns:
        - The Blog associated to the provided `slug`.
    """
    filters = []

    if slug:
        filters.append(blog_models.Blog.slug.ilike(other=slug))

    blog = blog_models.Blog.query.filter(*filters).first()
    if not blog:
        raise exceptions.DoesNotExist("Blog does not exist.")
    return blog


def get_blogs(author=None, category=None, published=None):
    """
    Get all blogs matching the provided keyword arguments.

    Params:
        `author` - Only blogs with this author will be returned. To get blogs
            with no author, use `0`.
        `category` - Only blogs with this category will be returned.
        `published` - Whether to return published or unpublished blogs.

    Returns:
        A list of Blogs.
    """
    filters = []

    if author is not None and author != 0:
        filters.append(blog_models.Blog.author == author)
    if author == 0:
        filters.append(blog_models.Blog.author is None)
    if category is not None:
        filters.append(
            blog_models.Blog.categories.any(
                category_models.Category.id.in_([category.id])
            )
        )
    if published is not None:
        filters.append(blog_models.Blog.published == published)

    blogs = (
        blog_models.Blog.query.filter(*filters)
        .order_by(blog_models.Blog.created_at.desc())
        .all()
    )
    return blogs


def retrieve_archived_blogs(published=None) -> dict:
    """
    Get a dictionary containing archived blogs sorted from oldest to newest.

    Args:
        published (bool, optional): Whether to return all, published or
        unpublished blogs. The default is all.

    Returns:
        dict: The first two integer keys represent the year and month (in that
        order) the blog posts were created.
    """
    blogs = get_blogs(published=published)
    blog_data = dict()
    for blog in blogs:
        date = blog.created_at.date()
        year = date.year
        month = date.month
        if not blog_data.get(year):
            blog_data.update({year: dict()})
        if not blog_data[year].get(month):
            blog_data[year].update({month: list()})
        blog_data[year][month].append(blog)
    return blog_data
