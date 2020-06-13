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
from unittest import mock

import pytest

from website.interfaces.common.templatetags import constants, filters


class TestFormatDatetime:
    @pytest.mark.parametrize(
        argnames="datetime,format,expected_function,expected_output",
        argvalues=[
            (
                datetime.datetime(year=2020, month=1, day=1),
                constants.BABEL_DATETIME_FORMAT_MEDIUM,
                "format_datetime",
                "1 Jan 2020, 00:00:00",
            ),
            (
                datetime.datetime(year=2020, month=1, day=1),
                None,
                "format_datetime",
                "1 Jan 2020, 00:00:00",
            ),
            (
                datetime.datetime(year=2020, month=1, day=1),
                constants.BABEL_DATETIME_FORMAT_TINY,
                "format_date",
                "1 Jan 2020",
            ),
        ],
    )
    @mock.patch(target="flask_babel.dates")
    def test_format_datetime_happy_path(
        self,
        mock_babel_dates,
        datetime,
        format,
        expected_function,
        expected_output,
    ):
        mocked_function = getattr(mock_babel_dates, expected_function)
        mocked_function.return_value = expected_output

        value = filters.format_datetime(datetime=datetime, format=format)

        assert value == expected_output


class TestFormatMonth:
    @pytest.mark.parametrize(
        argnames="month, expected", argvalues=[(1, "Jan"), (12, "Dec")],
    )
    @mock.patch.object(target=calendar, attribute="month_abbr")
    def test_format_month_happy_path(self, mock_month_abbr, month, expected):
        mock_month_abbr.__getitem__.return_value = expected

        value = filters.format_month(month=month)

        assert value == expected

    @pytest.mark.parametrize(
        argnames="month", argvalues=[0, 13],
    )
    def test_format_month_raises_error_when_invalid_month(self, month):
        with pytest.raises(expected_exception=filters.InvalidFormat) as e:
            filters.format_month(month=month)
        assert str(e.value) == "Month cannot be less than 1 or greater than 12"
