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

import flask
import flask_bouncer
import flask_login

from website.data.categories import models
from website.domain import exceptions
from website.domain.blogs import queries as blog_queries
from website.domain.categories import operations, queries
from website.interfaces.common.forms.categories import forms

categories = flask.Blueprint(
    name="categories", import_name=__name__, url_prefix="/categories"
)


@categories.route(rule="/<string:slug>")
def display(slug: str):
    try:
        category = queries.get_category(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    blogs = blog_queries.get_blogs(category=category, published=True)
    context = {
        "title": category.title,
        "category": category,
        "blogs": blogs,
    }
    return flask.render_template(
        template_name_or_list="categories/display.html", **context
    )


@categories.route(rule="/create", methods=["GET", "POST"])
@flask_login.login_required
@flask_bouncer.requires(action=flask_bouncer.CREATE, subject=models.Category)
def create():
    form = forms.Create()
    if form.validate_on_submit():
        try:
            category = operations.create_category(
                title=form.title.data, description=form.description.data
            )
        except exceptions.UnableToCreate:
            flask.flash(message="Unable to create category.", category="error")
            return flask.redirect(
                location=flask.url_for(endpoint="categories.create")
            )
        else:
            flask.flash(message="Category created.", category="success")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="categories.display", slug=category.slug
                )
            )
    context = {"title": "Create category", "form": form}
    return flask.render_template(
        template_name_or_list="categories/create.html", **context
    )


@categories.route(rule="/<string:slug>/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit(slug: str):
    try:
        category = queries.get_category(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=category)
    form = forms.Edit(obj=category)
    if form.validate_on_submit():
        try:
            operations.update_category(
                category=category,
                title=form.title.data,
                description=form.description.data,
            )
        except exceptions.UnableToUpdate:
            flask.flash(message="Unable to update category.", category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="categories.edit", slug=category.slug
                )
            )
        else:
            flask.flash(message="Category updated.", category="success")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="categories.display", slug=category.slug
                )
            )
    context = {"title": f"Edit {category.title}", "form": form}
    return flask.render_template(
        template_name_or_list="categories/edit.html", **context
    )


@categories.route(rule="/<string:slug>/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete(slug: str):
    try:
        category = queries.get_category(slug=slug)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.DELETE, subject=category)
    form = forms.Delete()
    if form.validate_on_submit():
        try:
            operations.delete_category(category=category)
        except exceptions.UnableToDelete:
            flask.flash(message="Unable to delete category.", category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="categories.display", slug=category.slug
                )
            )
        else:
            flask.flash(message="Category deleted.", category="success")
            return flask.redirect(
                location=flask.url_for(endpoint="main.landing")
            )
    context = {"title": f"Delete {category.title}", "form": form}
    return flask.render_template(
        template_name_or_list="categories/delete.html", **context
    )
