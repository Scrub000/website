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

import http
from typing import Optional

import flask
import flask_bouncer
import flask_login
import flask_restx
from flask import request
from flask_restx import fields

from website import decorators
from website.data.comments import models as models
from website.domain.blogs import queries as blog_queries
from website.domain.comments import operations, queries
from website.interfaces import api
from website.interfaces.api.comments import serializers

comments = flask.Blueprint(
    name="api-comments", import_name=__name__, url_prefix="/api/v1/comments",
)
api_comments = api.Api(
    app=comments,
    version="1.0",
    title="Comments API",
    description="API for comments, which currently relies on session cookies.",
)
comment_marshaller = api_comments.model(
    name="Comment", model=dict(body=fields.String),
)


class CommentDetail(flask_restx.Resource):
    serializer = serializers.Comment()

    def get(self, id: int):
        comment = queries.get_comment(id=id)
        return self.serializer.dump(obj=comment), http.HTTPStatus.OK

    @decorators.api_login_required
    def delete(self, id: int):
        comment = queries.get_comment(id=id)
        flask_bouncer.ensure(action=flask_bouncer.DELETE, subject=comment)
        comment.delete()
        return dict(), http.HTTPStatus.NO_CONTENT

    @decorators.api_login_required
    @api_comments.expect(comment_marshaller)
    def put(self, id: int):
        comment = queries.get_comment(id=id)
        flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=comment)
        payload = request.get_json(force=True)
        data = self.serializer.load(data=payload)
        operations.update_comment(comment=comment, **data)
        return self.serializer.dump(obj=comment), http.HTTPStatus.ACCEPTED


class CommentList(flask_restx.Resource):
    serializer = serializers.Comment()

    def get(
        self, blog_id: Optional[int] = None, parent_id: Optional[int] = None
    ):
        kwargs = dict()
        if blog_id:
            kwargs["blog"] = blog_queries.get_blog(id=blog_id)
        elif parent_id:
            kwargs["parent"] = queries.get_comment(id=parent_id)
        comments = queries.get_comments(**kwargs)
        return (
            self.serializer.dump(obj=comments, many=True),
            http.HTTPStatus.OK,
        )

    @decorators.api_login_required
    @api_comments.expect(comment_marshaller)
    def post(
        self, blog_id: Optional[int] = None, parent_id: Optional[int] = None
    ):
        flask_bouncer.ensure(
            action=flask_bouncer.CREATE, subject=models.Comment
        )
        payload = request.get_json(force=True)
        data = self.serializer.load(data=payload)
        data["author"] = flask_login.current_user
        if blog_id:
            data["blog"] = blog_queries.get_blog(id=blog_id)
        elif parent_id:
            data["parent"] = queries.get_comment(id=parent_id)
        comment = operations.create_comment(**data)
        return self.serializer.dump(obj=comment), http.HTTPStatus.CREATED


api_comments.add_resource(CommentDetail, "/<int:id>")
api_comments.add_resource(
    CommentList, "/list", "/blog/<int:blog_id>", "/parent/<int:parent_id>"
)
