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

import datetime

import flask
import flask_bouncer
import flask_login
import pytz

from website.comms import dispatch
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.domain.blogs import queries as blog_queries
from website.domain.categories import queries as category_queries
from website.interfaces.common.forms.main import forms

main = flask.Blueprint(name="main", import_name=__name__)


@main.route(rule="/")
def landing():
    blogs = blog_queries.get_blogs(published=True)
    context = {
        "title": "Blog",
        "blogs": blogs,
    }
    return flask.render_template(
        template_name_or_list="main/landing.html", **context
    )


@main.route(rule="/about")
def about():
    context = {"title": "About"}
    return flask.render_template(
        template_name_or_list="main/about.html", **context
    )


@main.route(rule="/archive")
def archive():
    blog_data = blog_queries.retrieve_archived_blogs(published=True)
    categories = category_queries.get_categories()
    context = {
        "title": "Archive",
        "blog_data": blog_data,
        "categories": categories,
    }
    return flask.render_template(
        template_name_or_list="main/archive.html", **context
    )


@main.route(rule="/contact", methods=["GET", "POST"])
def contact():
    form = forms.Contact()
    if form.validate_on_submit():
        flask.flash(message="Your enquiry has been sent.", category="success")
        dispatch.send_contact_email(
            email=form.email.data,
            enquiry=form.enquiry.data,
            body=form.body.data,
        )
        return flask.redirect(location=flask.url_for(endpoint="main.landing"))
    context = {"title": "Contact", "form": form}
    return flask.render_template(
        template_name_or_list="main/contact.html", **context
    )


@main.route(rule="/rss")
def rss():
    blogs = blog_queries.get_rss_blogs(published=True)
    response = flask.make_response(blogs)
    response.headers.set("Content-Type", "application/rss+xml")
    return response


##################
# Context handling
##################


@main.app_context_processor
def context_processor():
    actions = {
        "blogs": {
            "create": flask_bouncer.can(
                action=flask_bouncer.CREATE, subject=blog_models.Blog
            )
        },
        "categories": {
            "create": flask_bouncer.can(
                action=flask_bouncer.CREATE, subject=category_models.Category
            )
        },
    }
    return dict(link_actions=actions)


##################
# Request handling
##################


@main.before_app_request
def before_request():
    account = flask_login.current_user
    if account.is_authenticated:
        # TODO: Find a way to update this field, without updating the
        # updated_at field
        account.update(seen_at=datetime.datetime.now(tz=pytz.utc))


################
# Error handling
################


@main.app_errorhandler(code=404)
def not_found(error):
    context = {
        "title": "Page not found",
        "message": "This page does not exist on this server.",
    }
    return (
        flask.render_template(
            template_name_or_list="main/error.html", **context
        ),
        404,
    )


@main.app_errorhandler(code=403)
def permission_denied(error):
    context = {
        "title": "Permission denied",
        "message": "You do not have permission to view this page.",
    }
    return (
        flask.render_template(
            template_name_or_list="main/error.html", **context
        ),
        403,
    )


@main.app_errorhandler(code=500)
def internal_server_error(error):
    context = {
        "title": "Something went wrong",
        "message": "Something went wrong. Please try again later.",
    }
    return (
        flask.render_template(
            template_name_or_list="main/error.html", **context
        ),
        500,
    )
