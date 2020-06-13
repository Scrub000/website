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


from typing import Dict, List, Optional, Union

import flask
from feedgen import feed

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.domain import exceptions


def get_blog(
    id: Optional[int] = None, slug: Optional[str] = None
) -> blog_models.Blog:
    """
    Determine whether a Blog is available via the provided keyword arguments.

    Raises:
        - `DoesNotExist` if the Blog does not exist.
    Returns:
        - The Blog associated to the provided `id` or `slug`.
    """
    filters = []

    if id:
        filters.append(blog_models.Blog.id == id)
    if slug:
        filters.append(blog_models.Blog.slug.ilike(other=slug))

    blog = blog_models.Blog.query.filter(*filters).first()
    if not blog:
        raise exceptions.DoesNotExist("Blog does not exist.")
    return blog


def get_blogs(
    author: Optional[Union[account_models.Account, int]] = None,
    category: Optional[category_models.Category] = None,
    published: Optional[bool] = None,
) -> List[blog_models.Blog]:
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


def retrieve_archived_blogs(
    published: Optional[bool] = None,
) -> Dict[int, dict]:
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
    blog_data: Dict[int, dict] = dict()
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


def get_rss_blogs(
    author: Optional[Union[account_models.Account, int]] = None,
    category: Optional[category_models.Category] = None,
    published: Optional[bool] = None,
) -> str:
    """
    Return blogs in the RSS format.

    Params:
        `author` - Only blogs with this author will be returned. To get blogs
            with no author, use `0`.
        `category` - Only blogs with this category will be returned.
        `published` - Whether to return published or unpublished blogs.
    """
    host = flask.request.host_url[:-1]
    rss_url = flask.url_for(endpoint="main.rss")
    blogs = get_blogs(author=author, category=category, published=published)

    generator = _create_generator(host=host, blogs=blogs)
    generator.link(href=f"{host}{rss_url}", rel="self")

    return generator.rss_str()


# Private


def _create_generator(host: str, blogs: List[blog_models.Blog] = []):
    title = flask.current_app.config["FEED_TITLE"]
    description = flask.current_app.config["FEED_DESCRIPTION"]

    generator = feed.FeedGenerator()
    generator.title(title=title)
    generator.description(description=description)

    for blog in blogs:
        categories = list()
        blog_url = flask.url_for(endpoint="blogs.display", slug=blog.slug)
        author_url = flask.url_for(
            endpoint="accounts.display", username=blog.author.display
        )

        entry = generator.add_entry()
        entry.title(title=blog.title)
        entry.description(description=blog.description, isSummary=True)
        entry.content(content=blog.body)
        entry.guid(
            guid=f"{host}{blog_url}", permalink=True,
        )
        entry.author(
            name=blog.author.display,
            uri=f"{host}{author_url}",
            email=blog.author.email,
        )
        entry.published(published=blog.created_at)
        entry.updated(updated=blog.updated_at)

        for category in blog.categories:
            category_url = flask.url_for(
                endpoint="categories.display", slug=category.slug
            )
            category = dict(
                label=category.title,
                term=category.description,
                scheme=f"{host}{category_url}",
            )
            categories.append(category)
        entry.category(category=categories)
    return generator
