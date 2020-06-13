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
from unittest import mock

from website.domain import exceptions
from website.domain.blogs import queries, utils


class TestUniqueSlugify:
    @mock.patch.object(target=queries, attribute="get_blog")
    def test_unique_slug_generated_without_uuid(self, mock_get_blog):
        # ARRANGE
        mock_get_blog.side_effect = exceptions.DoesNotExist

        # ACT
        slug = utils.unique_slugify(text="blog")

        # ASSERT
        assert slug == "blog"

    @mock.patch.object(target=queries, attribute="get_blog")
    @mock.patch.object(target=uuid, attribute="uuid4")
    def test_unique_slug_generated_with_uuid(self, mock_uuid4, mock_get_blog):
        # ARRANGE
        mock_get_blog.side_effect = [mock.Mock(), exceptions.DoesNotExist]
        mock_uuid4.return_value = mock.Mock(
            hex="a12c6af1-144d-4f88-b467-e06e3f3e3d47"
        )

        # ACT
        slug = utils.unique_slugify(text="blog")

        # ASSERT
        assert slug == "a12-blog"

    @mock.patch.object(target=queries, attribute="get_blog")
    def test_unique_slug_generated_with_max_length(self, mock_get_blog):
        # ARRANGE
        mock_get_blog.side_effect = exceptions.DoesNotExist

        # ACT
        slug = utils.unique_slugify(text="blog", max_length=3)

        # ASSERT
        assert slug == "blo"
