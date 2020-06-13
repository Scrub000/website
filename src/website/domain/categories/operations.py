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

from website.data.categories import models
from website.domain import exceptions, utils


def create_category(title: str, description: str) -> models.Category:
    """
    Create a Category in the database.

    Raises:
        - `UnableToCreate` if Category cannot be created.

    Returns:
        - A new Category.
    """
    try:
        slug = utils.unique_slugify(
            model=models.Category, text=title, max_length=200
        )
    except exceptions.UnableToGenerateSlug:
        raise exceptions.UnableToCreate("Unable to create category.")
    try:
        category = models.Category.new(
            title=title, slug=slug, description=description,
        )
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToCreate("Unable to create category.")

    # TODO: Publish an event

    return category


def update_category(category: models.Category, **kwargs):
    """
    Update a Category in the database.

    Raises:
        - `UnableToUpdate` if Category cannot be updated.
    """
    try:
        category.update(**kwargs)
    except Exception:
        # TODO: Publish an event
        raise exceptions.UnableToUpdate("Unable to update category.")

    # TODO: Publish an event


def delete_category(category: models.Category):
    """
    Delete a Category from the database.
    """
    try:
        category.delete()
    except Exception:
        raise exceptions.UnableToDelete("Unable to delete category.")

    # TODO: Send comms emails

    # TODO: Publish an event
