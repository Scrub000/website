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


from ...data.categories import models
from .. import exceptions


def get_category(slug: str = None) -> models.Category:
    """
    Determine whether a Category is available via the provided keyword
    arguments.

    Raises:
        - `DoesNotExist` if the Category does not exist.
    Returns:
        - The Category associated to the provided `slug`.
    """
    filters = []

    if slug:
        filters.append(models.Category.slug.ilike(other=slug))
    category = models.Category.query.filter(*filters).first()

    if not category:
        raise exceptions.DoesNotExist("Category does not exist.")
    return category


def get_categories() -> list:
    """
    Retrieve all categories.

    Returns:
        - Optional list of [Category]
    """
    return models.Category.query.order_by(models.Category.title.desc()).all()
