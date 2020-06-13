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

import flask
import flask_bouncer
import flask_login
import flask_restx
from flask import request
from flask_restx import fields

from website import decorators
from website.data.blogs import models
from website.domain.blogs import operations, queries
from website.interfaces import api
from website.interfaces.api.blogs import serializers

blogs = flask.Blueprint(
    name="api-blogs", import_name=__name__, url_prefix="/api/v1/blogs",
)
api_blogs = api.Api(
    app=blogs,
    version="1.0",
    title="Blogs API",
    description="API for blogs, which currently relies on session cookies.",
)
blog_marshaller = api_blogs.model(
    name="Blog",
    model=dict(
        title=fields.String,
        description=fields.String,
        body=fields.String,
        published=fields.Boolean,
        categories=fields.List(cls_or_instance=fields.Integer),
    ),
)


class BlogDetail(flask_restx.Resource):
    serializer = serializers.Blog()

    def get(self, id: int):
        blog = queries.get_blog(id=id)
        return self.serializer.dump(obj=blog), http.HTTPStatus.OK

    @decorators.api_login_required
    def delete(self, id: int):
        blog = queries.get_blog(id=id)
        flask_bouncer.ensure(action=flask_bouncer.DELETE, subject=blog)
        blog.delete()
        return dict(), http.HTTPStatus.NO_CONTENT

    @decorators.api_login_required
    @api_blogs.expect(blog_marshaller)
    def put(self, id: int):
        blog = queries.get_blog(id=id)
        flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=blog)
        payload = request.get_json(force=True)
        data = self.serializer.load(data=payload)
        operations.update_blog(blog=blog, **data)
        return self.serializer.dump(obj=blog), http.HTTPStatus.ACCEPTED


class BlogList(flask_restx.Resource):
    serializer = serializers.Blog()

    def get(self):
        blogs = queries.get_blogs(published=True)
        return (
            self.serializer.dump(obj=blogs, many=True),
            http.HTTPStatus.OK,
        )

    @decorators.api_login_required
    @api_blogs.expect(blog_marshaller)
    def post(self):
        flask_bouncer.ensure(action=flask_bouncer.CREATE, subject=models.Blog)
        payload = request.get_json(force=True)
        data = self.serializer.load(data=payload)
        data["author"] = flask_login.current_user
        blog = operations.create_blog(**data)
        return self.serializer.dump(obj=blog), http.HTTPStatus.CREATED


api_blogs.add_resource(BlogDetail, "/<int:id>")
api_blogs.add_resource(BlogList, "/list")
