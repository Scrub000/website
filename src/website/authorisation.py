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

import flask_bouncer
from bouncer import models as bouncer_models

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models


def define_authorisation(
    account: account_models.Account, they: bouncer_models.RuleList
):
    if account.is_authenticated:
        if account.is_admin:
            # Admins can do anything
            they.can(action=flask_bouncer.MANAGE, subject=flask_bouncer.ALL)
        elif account.is_confirmed:
            # Confirmed accounts can read, edit and delete their own account
            they.can(
                action=(
                    flask_bouncer.READ,
                    flask_bouncer.EDIT,
                    flask_bouncer.DELETE,
                ),
                subject=account_models.Account,
                id=account.id,
            )
            # Confirmed accounts can create blogs
            they.can(action=flask_bouncer.CREATE, subject=blog_models.Blog)
            # Confirmed accounts can read, edit and delete their own blogs
            they.can(
                action=(
                    flask_bouncer.READ,
                    flask_bouncer.EDIT,
                    flask_bouncer.DELETE,
                ),
                subject=blog_models.Blog,
                author_id=account.id,
            )
    # Any account can read accounts and categories
    they.can(
        action=flask_bouncer.READ,
        subject=(account_models.Account, category_models.Category),
    )
    # Any account can read published blogs
    they.can(
        action=flask_bouncer.READ, subject=blog_models.Blog, published=True
    )
