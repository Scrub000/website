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

from website import marshmallow
from website.data.comments import models


class Comment(marshmallow.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for the Comment model. All attributes, except for the body, are
    read-only.
    """

    id = marshmallow.auto_field(dump_only=True)
    body = marshmallow.auto_field()
    path = marshmallow.auto_field(dump_only=True)
    created_at = marshmallow.auto_field(dump_only=True)
    updated_at = marshmallow.auto_field(dump_only=True)
    thread_at = marshmallow.auto_field(dump_only=True)
    author = marshmallow.auto_field(dump_only=True)
    blog = marshmallow.auto_field(dump_only=True)
    parent = marshmallow.auto_field(dump_only=True)
    replies = marshmallow.auto_field(dump_only=True)

    class Meta:
        fields = (
            "id",
            "body",
            "path",
            "created_at",
            "updated_at",
            "thread_at",
            "author",
            "blog",
            "parent",
            "replies",
        )
        model = models.Comment
