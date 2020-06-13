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

import uuid

import slugify

from ...domain import exceptions
from . import queries

UUID_LENGTH = 3


def unique_slugify(text: str, max_length: int = 0) -> str:
    """
    Generate a unique slug based on the provided text.

    Raises:
        `UnableToGenerateSlug` if slug cannot be generated.
    """
    slug = slugify.slugify(text=text, max_length=max_length)

    try:
        _ = queries.get_blog(slug=slug)
    except exceptions.DoesNotExist:
        pass
    else:
        try:
            uuid_text = uuid.uuid4().hex[:UUID_LENGTH].lower()
            # UUID text comes first, as to not cut off the unique text if the
            # max_length is too short
            new_text = f"{uuid_text}-{text}"
            slug = unique_slugify(text=new_text, max_length=max_length)
        except RecursionError:
            raise exceptions.UnableToGenerateSlug(
                "Unable to generate unique slug."
            )
    return slug
