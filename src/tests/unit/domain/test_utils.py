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

import uuid
from unittest import mock

import pytest
from sqlalchemy.orm import attributes as sqlalchemy_attributes

from website.domain import exceptions, utils


class TestUniqueSlugify:
    def test_unique_slug_generated_without_uuid(self):
        # ARRANGE
        model = self._setup_valid_model()
        model.query.filter_by.return_value.first.return_value = None

        # ACT
        slug = utils.unique_slugify(model=model, text="My blog")

        # ASSERT
        assert slug == "my-blog"

    @mock.patch.object(target=uuid, attribute="uuid4")
    def test_unique_slug_generated_with_uuid(self, mock_uuid4):
        # ARRANGE
        model = self._setup_valid_model()
        model.query.filter_by.return_value.first.side_effect = [
            mock.Mock(),
            None,
        ]
        mock_uuid4.return_value = mock.Mock(
            hex="a12c6af1-144d-4f88-b467-e06e3f3e3d47"
        )

        # ACT
        slug = utils.unique_slugify(model=model, text="My blog")

        # ASSERT
        assert slug == "a12-my-blog"

    def test_unique_slug_generated_with_max_length(self):
        # ARRANGE
        model = self._setup_valid_model()
        model.query.filter_by.return_value.first.return_value = None

        # ACT
        slug = utils.unique_slugify(model=model, text="My blog", max_length=4)

        # ASSERT
        assert slug == "my-b"

    def test_recursion_error_raises_exception(self):
        # ARRANGE
        model = self._setup_valid_model()

        # ACT & ASSERT
        with pytest.raises(
            expected_exception=exceptions.UnableToGenerateSlug
        ) as exception:
            utils.unique_slugify(model=model, text="My blog")
        assert str(exception.value) == "Unable to generate unique slug"

    def test_model_raises_when_missing_correct_slug_attribute(self):
        # ARRANGE
        model = mock.Mock(slug="Not an InstrumentedAttribute")

        # ACT & ASSERT
        with pytest.raises(
            expected_exception=exceptions.UnableToGenerateSlug
        ) as exception:
            utils.unique_slugify(model=model, text="My blog")
        assert str(exception.value) == "Model does not have the slug attribute"

    # Private

    def _setup_valid_model(self):
        slug = mock.Mock(spec=sqlalchemy_attributes.InstrumentedAttribute)
        model = mock.Mock(slug=slug)
        return model
