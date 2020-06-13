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

import datetime
from unittest import mock

from website.domain.blogs import queries


class TestRetrieveArchivedBlogs:
    @mock.patch.object(target=queries, attribute="get_blogs")
    def test_blogs_have_correct_format(self, mock_get_blogs):
        newest_blog = mock.Mock(
            created_at=datetime.datetime(year=2020, month=1, day=6)
        )
        midway_blog = mock.Mock(
            created_at=datetime.datetime(year=2020, month=1, day=1)
        )
        oldest_blog = mock.Mock(
            created_at=datetime.datetime(year=2019, month=5, day=1)
        )
        mock_get_blogs.return_value = [newest_blog, midway_blog, oldest_blog]

        data = queries.retrieve_archived_blogs()

        assert data == {
            2020: {1: [newest_blog, midway_blog]},
            2019: {5: [oldest_blog]},
        }
