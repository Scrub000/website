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

import http

import flask
import flask_restx
from marshmallow import exceptions as marshmallow_exceptions
from werkzeug import exceptions as werkzeug_exceptions
from werkzeug import http as werkzeug_http

from website.domain import exceptions


class Api(flask_restx.Api):
    def handle_error(self, error):
        """
        Custom `handle_error` function which will help to prevent writing
        unnecessary try/except blocks throughout the API.
        """
        # Handle HTTPExceptions
        if isinstance(error, werkzeug_exceptions.HTTPException):
            message = werkzeug_http.HTTP_STATUS_CODES.get(error.code, "")
            return (
                flask.jsonify(dict(message=message)),
                error.code,
            )
        # If the error is from any of our custom exceptions, handle them
        if any(
            [
                isinstance(error, exception)
                for exception in [
                    exceptions.UnableToCreate,
                    exceptions.UnableToDelete,
                    exceptions.UnableToGenerateSlug,
                    exceptions.UnableToUpdate,
                ]
            ]
        ):
            return (
                flask.jsonify(dict(message=str(error))),
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        if isinstance(error, exceptions.DoesNotExist):
            return (
                flask.jsonify(dict(message=str(error))),
                http.HTTPStatus.NOT_FOUND,
            )
        # Handle marshmallow exceptions
        if isinstance(error, marshmallow_exceptions.ValidationError):
            return (
                flask.jsonify(error.messages),
                http.HTTPStatus.BAD_REQUEST,
            )
        # If the message attribute is not set, consider it as a Python core
        # exception and hide sensitive error info from the end-user
        if not getattr(error, "message", None):
            print(f"Unhandled exception in API: {error}")
            return (
                flask.jsonify(
                    dict(message="Something went wrong on our server.")
                ),
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        # Handle application specific custom exceptions
        return flask.jsonify(**error.kwargs), error.http_status_code
