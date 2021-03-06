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

from website import admin, db
from website.data.accounts import models
from website.interfaces.admin import base


class AccountModelView(base.ModelView):
    can_create = False
    can_delete = False
    column_default_sort = ("created_at", True)
    column_exclude_list = ["password"]
    column_editable_list = ["display", "about", "admin", "confirmed"]
    column_searchable_list = ["username", "email"]
    column_filters = ["admin", "confirmed"]
    form_excluded_columns = ["username", "email", "password", "blogs"]
    page_size = 50


admin.add_view(
    view=AccountModelView(
        category=base.CATEGORY_ACCOUNT_MANAGEMENT,
        model=models.Account,
        session=db.session,
    )
)
