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
from website.data.accounts import models

from . import model_factory

__all__ = ["Account", "create_account_with_blogs"]


class Account(model_factory.Base):
    """
    Create a default account with no blog posts.
    """

    username = factory.Faker("user_name")
    display = factory.Faker("name")
    email = factory.Faker("safe_email")
    about = factory.Faker("text", max_nb_chars=200)
    password = factory.PostGenerationMethodCall(
        method_name="update", password="password"
    )
    admin = False
    confirmed = False

    class Meta:
        model = models.Account


def create_account_with_blogs(blog_kwargs: dict = {}) -> models.Account:
    blog = factories.Blog(**blog_kwargs)
    account = blog.author
    factories.Blog(author=account, **blog_kwargs)
    return account
