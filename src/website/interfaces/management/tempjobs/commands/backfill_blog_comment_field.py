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

from typing import List

import click
from flask import cli

from website.data.blogs import models


@click.command(name="backfill_blog_comment_field")
@click.option(
    "--not-dry-run",
    default=False,
    is_flag=True,
    help="Run this command for real",
)
@cli.with_appcontext
def command(not_dry_run: bool):
    blogs: List[models.Blog] = models.Blog.query.all()
    blogs_to_update: int = len(blogs)
    print(f"Updating {blogs_to_update} blogs.")
    for blog in blogs:
        blog.update(comment=True)
