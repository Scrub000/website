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

import functools

import flask
import flask_login


def login_forbidden(view_func, redirect_endpoint="main.landing"):
    """
    Redirect logged in users.
    """

    @functools.wraps(view_func)
    def decorated_function(*args, **kwargs):
        if flask_login.current_user.is_authenticated:
            flask.flash(
                message="Only unauthenticated users can view this page.",
                category="warning",
            )
            return flask.redirect(
                location=flask.url_for(endpoint=redirect_endpoint)
            )
        return view_func(*args, **kwargs)

    return decorated_function
