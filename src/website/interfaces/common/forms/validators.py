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

import slugify
import sqlalchemy
from wtforms import validators


class Base(object):
    """
    Base validator object.
    """

    def __init__(self, model, field, message=u"This field is not valid."):
        self.model = model
        self.field = field
        self.message = message


class Unique(Base):
    """
    Validates a field to ensure that it is unique within the database.

    :param model:
        Model to be validated against.
    :param field:
        Field which will be validated.
    :param message:
        Error message to raise in case of a validation error.
    """

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise validators.ValidationError(self.message)


class IUnique(Base):
    """
    Validates a field to ensure that it is unique within the database. This is
    similar to the `Unique` validator, however it is case-insensitive.

    :param model:
        Model to be validated against.
    :param field:
        Field which will be validated.
    :param message:
        Error message to raise in case of a validation error.
    """

    def __call__(self, form, field):
        check = self.model.query.filter(
            sqlalchemy.func.lower(self.field)
            == sqlalchemy.func.lower(field.data)
        ).first()
        if check:
            raise validators.ValidationError(self.message)


class Slug(Base):
    """
    Validates a field to ensure that it is a valid slug.

    :param model:
        Model to be validated against.
    :param field:
        Field which will be validated.
    :param message:
        Error message to raise in case of a validation error.
    """

    def __call__(self, form, field):
        original_slug = field.data
        slugified_slug = slugify.slugify(original_slug)

        if original_slug != slugified_slug:
            raise validators.ValidationError(self.message)
