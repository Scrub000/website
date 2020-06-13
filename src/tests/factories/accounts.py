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

import factory

from website.data.accounts import models

from . import model_factory


class Account(model_factory.Base):
    """
    Create a default account with no blog posts.
    """

    class Meta:
        model = models.Account

    username = "gough"
    display = "Gough Whitlam"
    email = "gough.whitlam@alp.org.au"
    password = factory.PostGenerationMethodCall(
        method_name="update", password="It's time"
    )
    confirmed = False
