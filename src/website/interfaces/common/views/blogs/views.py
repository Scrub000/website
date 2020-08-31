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

import bleach
import flask
import flask_bouncer
import flask_login

from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.domain import exceptions
from website.domain.blogs import operations, queries
from website.interfaces import constants
from website.interfaces.common.forms.blogs import forms

blogs = flask.Blueprint(
    name="blogs", import_name=__name__, url_prefix="/blogs"
)


@blogs.route(rule="/<string:slug>")
def display(slug: str):
    try:
        blog = queries.get_blog(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.READ, subject=blog)
    form = comment_forms.Create()
    if form.validate_on_submit():
        try:
            comment_operations.create_comment(
                body=form.body.data, author=flask_login.current_user, blog=blog
            )
        except exceptions.UnableToCreate as e:
            flask.flash(message=str(e), category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="blogs.display", slug=blog.slug
                )
            )
        else:
            return flask.redirect(
                location=flask.url_for(
                    endpoint="blogs.display", slug=blog.slug
                )
            )
    comments = comment_queries.get_comments(blog=blog)
    context = {
        "title": blog.title,
        "blog": blog,
        "form": form,
        "comments": comments,
    }
    return flask.render_template(
        template_name_or_list="blogs/display.html", **context
    )


@blogs.route(rule="/create", methods=["GET", "POST"])
@flask_login.login_required
@flask_bouncer.requires(action=flask_bouncer.CREATE, subject=blog_models.Blog)
def create():
    form = forms.Create()
    form.categories.query = category_models.Category.query.all()
    if form.validate_on_submit():
        try:
            blog = operations.create_blog(
                title=form.title.data,
                body=bleach.clean(
                    text=form.body.data, **constants.BLEACH_KWARGS
                ),
                description=form.description.data,
                author=flask_login.current_user,
                categories=form.categories.data,
                published=form.published.data,
                comment=form.comment.data,
            )
        except exceptions.UnableToCreate:
            flask.flash(message="Unable to create blog.", category="error")
            return flask.redirect(
                location=flask.url_for(endpoint="blogs.create")
            )
        else:
            flask.flash(message="Blog created.", category="success")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="blogs.display", slug=blog.slug
                )
            )
    context = {"title": "Create blog", "form": form}
    return flask.render_template(
        template_name_or_list="blogs/create.html", **context
    )


@blogs.route(rule="/<string:slug>/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit(slug: str):
    try:
        blog = queries.get_blog(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=blog)
    form = forms.Edit(obj=blog)
    form.categories.query = category_models.Category.query.all()
    if form.validate_on_submit():
        try:
            operations.update_blog(
                blog=blog,
                title=form.title.data,
                description=form.description.data,
                body=bleach.clean(
                    text=form.body.data, **constants.BLEACH_KWARGS
                ),
                categories=form.categories.data,
                published=form.published.data,
                comment=form.comment.data,
            )
        except exceptions.UnableToUpdate:
            flask.flash(message="Unable to update blog.", category="error")
            return flask.redirect(
                location=flask.url_for(endpoint="blogs.edit", slug=blog.slug)
            )
        else:
            flask.flash(message="Blog updated.", category="success")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="blogs.display", slug=blog.slug
                )
            )
    context = {"title": f"Edit {blog.title}", "form": form}
    return flask.render_template(
        template_name_or_list="blogs/edit.html", **context
    )


@blogs.route(rule="/<string:slug>/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete(slug: str):
    try:
        blog = queries.get_blog(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.DELETE, subject=blog)
    form = forms.Delete()
    if form.validate_on_submit():
        try:
            operations.delete_blog(blog=blog)
        except exceptions.UnableToDelete:
            flask.flash(message="Unable to delete blog.", category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="blogs.display", slug=blog.slug
                )
            )
        else:
            flask.flash(message="Blog deleted.", category="success")
            return flask.redirect(
                location=flask.url_for(endpoint="main.landing")
            )
    context = {"title": f"Delete {blog.title}", "form": form}
    return flask.render_template(
        template_name_or_list="blogs/delete.html", **context
    )
