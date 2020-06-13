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

import wtforms

from website import admin, db
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.domain import utils
from website.interfaces.admin import base


class BlogModelView(base.ModelView):
    can_view_details = True
    column_default_sort = ("created_at", True)
    column_editable_list = ["title", "description", "published"]
    column_searchable_list = ["title", "description"]
    column_exclude_list = ["body"]
    column_filters = ["published"]
    form_excluded_columns = ["slug"]
    form_overrides = dict(slug=wtforms.StringField)
    page_size = 50

    def on_model_change(self, form, model, is_created):
        if is_created:
            # Required as we're querying the database
            # https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.no_autoflush
            with db.session.no_autoflush:
                slug = utils.unique_slugify(
                    model=blog_models.Blog, text=model.title, max_length=200
                )
            model.slug = slug


class CategoryModelView(base.ModelView):
    column_default_sort = ("created_at", True)
    column_editable_list = ["title", "description"]
    column_searchable_list = ["title", "description"]
    form_excluded_columns = ["slug", "blogs"]
    form_overrides = dict(slug=wtforms.StringField)
    page_size = 50

    def on_model_change(self, form, model, is_created):
        if is_created:
            # Required as we're querying the database
            # https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.no_autoflush
            with db.session.no_autoflush:
                slug = utils.unique_slugify(
                    model=category_models.Category,
                    text=model.title,
                    max_length=200,
                )
            model.slug = slug


admin.add_view(
    view=BlogModelView(
        category=base.CATEGORY_BLOG_MANAGEMENT,
        model=blog_models.Blog,
        session=db.session,
    )
)
admin.add_view(
    view=CategoryModelView(
        category=base.CATEGORY_BLOG_MANAGEMENT,
        model=category_models.Category,
        session=db.session,
    )
)
