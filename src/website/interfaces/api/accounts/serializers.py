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
from website.data.accounts import models


class Account(marshmallow.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for the Account model. Sensitive attributes, such as the ID,
    username or statuses, are read-only. Personal attributes, such as the email
    or hashed password, are not included.
    """

    id = marshmallow.auto_field(dump_only=True)
    username = marshmallow.auto_field(dump_only=True)
    display = marshmallow.auto_field()
    about = marshmallow.auto_field()
    admin = marshmallow.auto_field(dump_only=True)
    confirmed = marshmallow.auto_field(dump_only=True)
    created_at = marshmallow.auto_field(dump_only=True)
    updated_at = marshmallow.auto_field(dump_only=True)
    seen_at = marshmallow.auto_field(dump_only=True)

    class Meta:
        fields = (
            "id",
            "username",
            "display",
            "about",
            "admin",
            "confirmed",
            "created_at",
            "updated_at",
            "seen_at",
        )
        model = models.Account
