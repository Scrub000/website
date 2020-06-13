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

import flask
import flask_login
from flask_admin import form
from flask_admin.contrib import sqla

CATEGORY_ACCOUNT_MANAGEMENT = "Account management"
CATEGORY_BLOG_MANAGEMENT = "Blog management"


class ModelView(sqla.ModelView):
    """
    Modified sqla.ModelView class which enables CSRF protection for the forms,
    and restricts who can access views to only administrators.
    """

    form_base_class = form.SecureForm

    def is_accessible(self):
        return (
            flask_login.current_user.is_authenticated
            and flask_login.current_user.is_admin
        )

    def inaccessible_callback(self, name, **kwargs):
        flask.flash(
            message="You do not have the permission to access this page.",
            category="error",
        )
        return flask.redirect(location=flask.url_for(endpoint="main.landing"))
