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

import calendar
import datetime
from typing import Union

import flask
import flask_babel

from website.interfaces.common.templatetags import constants

filters = flask.Blueprint(name="filters", import_name=__name__)


class InvalidFormat(Exception):
    pass


@filters.app_template_filter(name="formatdatetime")
def format_datetime(
    datetime: Union[datetime.date, datetime.datetime],
    format: str = constants.BABEL_DATETIME_FORMAT_MEDIUM,
):
    """
    Template tag which uses Babel to render a specified datetime. The default
    format is `BABEL_DATETIME_FORMAT_MEDIUM`.
    """
    format = f"{format}".lower()
    if format not in [
        constants.BABEL_DATETIME_FORMAT_FULL,
        constants.BABEL_DATETIME_FORMAT_LONG,
        constants.BABEL_DATETIME_FORMAT_MEDIUM,
        constants.BABEL_DATETIME_FORMAT_SHORT,
        constants.BABEL_DATETIME_FORMAT_TINY,
    ]:
        format = constants.BABEL_DATETIME_FORMAT_MEDIUM
    if format == constants.BABEL_DATETIME_FORMAT_TINY:
        return flask_babel.dates.format_date(
            date=datetime, format=constants.BABEL_DATETIME_FORMAT_MEDIUM
        )
    return flask_babel.dates.format_datetime(datetime=datetime, format=format)


@filters.app_template_filter(name="formatmonth")
def format_month(month: int) -> str:
    """
    Template tag which uses the Calendar API to return the abbreviated version
    of the specified `month`.
    """
    if month < 1 or month > 12:
        raise InvalidFormat("Month cannot be less than 1 or greater than 12")
    return calendar.month_abbr[month]
