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

from website import marshmallow
from website.data.blogs import models
from website.interfaces.api import fields as api_fields


class Blog(marshmallow.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for the Blog model. Sensitive attributes, such as the ID, slug,
    author or statuses, are read-only.
    """

    id = marshmallow.auto_field(dump_only=True)
    title = marshmallow.auto_field()
    slug = marshmallow.auto_field(dump_only=True)
    description = marshmallow.auto_field()
    body = api_fields.HTML()
    published = marshmallow.auto_field()
    created_at = marshmallow.auto_field(dump_only=True)
    updated_at = marshmallow.auto_field(dump_only=True)
    author = marshmallow.auto_field(dump_only=True)
    categories = marshmallow.auto_field()

    class Meta:
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "body",
            "published",
            "created_at",
            "updated_at",
            "author",
            "categories",
        )
        model = models.Blog
