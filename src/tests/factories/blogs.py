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

import factory

from tests import factories
from website.data.blogs import models
from website.domain import utils

from . import model_factory


class Blog(model_factory.Base):
    """
    Create a blog post with an author.
    """

    title = factory.Faker("catch_phrase")
    slug = factory.LazyAttribute(
        lambda o: utils.unique_slugify(
            model=models.Blog, text=o.title, max_length=200
        )
    )
    description = factory.Faker("text", max_nb_chars=200)
    body = factory.Faker("text", max_nb_chars=2000)
    published = False
    comment = False
    author = factory.SubFactory(factory=factories.Account)

    class Meta:
        model = models.Blog
