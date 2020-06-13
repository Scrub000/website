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

import bleach
from marshmallow import fields

from website.interfaces import constants


class HTML(fields.Field):
    """
    Field that serializes to a string HTML content, and deserializes to a
    string of cleaned HTML content. For example, if the HTML tag `h6` was not
    allowed, we would deserialize `"<h6>Test</h6>"` to
    `"&lt;h6&gt;Test&lt;/h6&gt;"`.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return ""
        return bleach.clean(text=value, **constants.BLEACH_KWARGS)
