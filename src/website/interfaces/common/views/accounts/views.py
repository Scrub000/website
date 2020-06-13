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
import flask_bouncer
import flask_login

from website import decorators
from website.comms import dispatch
from website.domain import exceptions
from website.domain.accounts import operations, queries, utils
from website.domain.blogs import queries as blog_queries
from website.interfaces.common.forms.accounts import forms

accounts = flask.Blueprint(
    name="accounts", import_name=__name__, url_prefix="/account"
)


@accounts.route(rule="/<string:username>")
def display(username: str):
    try:
        account = queries.get_account(username=username)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    blogs = blog_queries.get_blogs(author=account, published=True)
    context = {
        "title": account.display,
        "account": account,
        "blogs": blogs,
    }
    return flask.render_template(
        template_name_or_list="accounts/display.html", **context
    )


@accounts.route(rule="/<string:username>/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit(username: str):
    try:
        account = queries.get_account(username=username)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=account)
    form = forms.Edit(obj=account)
    if form.validate_on_submit():
        try:
            operations.update_account(
                account=account,
                display=form.display.data,
                about=form.about.data,
            )
        except exceptions.UnableToUpdate:
            flask.flash(message="Unable to edit account.", category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="accounts.edit", username=account.username
                )
            )
        else:
            flask.flash(
                message="Account updated.", category="success",
            )
            return flask.redirect(
                location=flask.url_for(
                    endpoint="accounts.display", username=account.username
                )
            )
    context = {"title": f"Edit {account.display}", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/edit.html", **context
    )


@accounts.route(rule="/<string:username>/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete(username: str):
    try:
        account = queries.get_account(username=username)
    except exceptions.DoesNotExist:
        flask.abort(status=404)
    flask_bouncer.ensure(action=flask_bouncer.DELETE, subject=account)
    form = forms.Delete()
    if form.validate_on_submit():
        try:
            operations.delete_account(
                account=account, delete_blogs=form.delete_blogs.data
            )
        except exceptions.UnableToDelete:
            flask.flash(message="Unable to delete account.", category="error")
            return flask.redirect(
                location=flask.url_for(
                    endpoint="accounts.display", username=account.username
                )
            )
        else:
            flask.flash(message="Account deleted.", category="success")
            if flask_login.current_user == account:
                flask_login.logout_user()
            return flask.redirect(
                location=flask.url_for(endpoint="main.landing")
            )
    context = {"title": f"Delete {account.display}", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/delete.html", **context
    )


@accounts.route(rule="/login", methods=["GET", "POST"])
@decorators.login_forbidden
def login():
    form = forms.Login()
    if form.validate_on_submit():
        try:
            account = queries.check_login(
                email=form.email.data, password=form.password.data
            )
        except (exceptions.DoesNotExist, exceptions.InvalidPassword):
            flask.flash(
                message="Your email and/or password is incorrect.",
                category="error",
            )
            return flask.redirect(
                location=flask.url_for(endpoint="accounts.login")
            )
        except exceptions.EmailNotConfirmed:
            endpoint = flask.url_for(endpoint="accounts.request_confirm_email")
            flask.flash(
                message="Your email has not been confirmed.", category="error",
            )
            flask.flash(
                message=flask.Markup(
                    (
                        f'Click <a href="{endpoint}">here</a> to re-send a '
                        "confirmation email."
                    )
                ),
                category="info",
            )
            return flask.redirect(
                location=flask.url_for(endpoint="accounts.login")
            )
        else:
            flask.flash(
                message=f"Logged in as {account.display}.", category="success"
            )
            flask_login.login_user(
                user=account, remember=form.remember_me.data
            )
            return flask.redirect(
                location=flask.url_for(endpoint="main.landing")
            )
    context = {"title": "Log in", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/login.html", **context
    )


@accounts.route(rule="/register", methods=["GET", "POST"])
@decorators.login_forbidden
def register():
    form = forms.Register()
    if form.validate_on_submit():
        try:
            operations.create_account(
                username=form.username.data,
                display=form.display.data,
                email=form.email.data,
                password=form.password.data,
            )
        except exceptions.UnableToCreate:
            flask.flash(
                message="Unable to register account.", category="error"
            )
            return flask.redirect(
                location=flask.url_for(endpoint="accounts.register")
            )
        else:
            flask.flash(
                message=(
                    "Account registered. Please check your email to confirm "
                    "your account."
                ),
                category="success",
            )
            return flask.redirect(
                location=flask.url_for(endpoint="accounts.login")
            )
    context = {"title": "Register", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/register.html", **context
    )


@accounts.route(rule="/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for(endpoint="main.landing"))


@accounts.route(rule="/request-confirm-email", methods=["GET", "POST"])
@decorators.login_forbidden
def request_confirm_email():
    form = forms.EmailRequest()
    if form.validate_on_submit():
        try:
            account = queries.get_account(email=form.email.data)
        except exceptions.DoesNotExist:
            flask.flash(message="This email does not exist.", category="error")
        else:
            if not account.is_confirmed:
                flask.flash(
                    message="Confirmation email has been sent.",
                    category="success",
                )
                dispatch.send_confirm_account_email(account=account)
            else:
                flask.flash(
                    message="Account is already confirmed.", category="error"
                )
        return flask.redirect(
            location=flask.url_for(endpoint="accounts.login")
        )
    context = {"title": "Re-send confirmation email", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/email_request.html", **context
    )


@accounts.route(rule="/confirm-email/<string:token>")
@decorators.login_forbidden
def confirm_email(token: str):
    account = utils.verify_confirm_email_token(token=token)
    if not account:
        flask.flash(
            message="Token is either invalid or expired.", category="error"
        )
        return flask.redirect(
            location=flask.url_for(endpoint="accounts.login")
        )
    flask.flash(message="Email confirmed.", category="success")
    account.update(confirmed=True)
    return flask.redirect(location=flask.url_for(endpoint="accounts.login"))


@accounts.route(rule="/request-reset-password", methods=["GET", "POST"])
@decorators.login_forbidden
def request_reset_password():
    form = forms.EmailRequest()
    if form.validate_on_submit():
        try:
            account = queries.get_account(email=form.email.data)
        except exceptions.DoesNotExist:
            flask.flash(message="This email does not exist.", category="error")
        else:
            flask.flash(
                message="Reset password email has been sent.",
                category="success",
            )
            dispatch.send_reset_password_email(account=account)
        return flask.redirect(
            location=flask.url_for(endpoint="accounts.login")
        )
    context = {"title": "Reset password", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/email_request.html", **context
    )


@accounts.route(rule="/reset-password/<string:token>", methods=["GET", "POST"])
@decorators.login_forbidden
def reset_password(token: str):
    account = utils.verify_reset_password_token(token=token)
    if not account:
        flask.flash(
            message="Token is either invalid or expired.", category="error"
        )
        return flask.redirect(
            location=flask.url_for(endpoint="accounts.login")
        )
    form = forms.ResetPassword()
    if form.validate_on_submit():
        account.update(password=form.password.data)
        flask.flash(message="Password has been reset.", category="success")
        return flask.redirect(
            location=flask.url_for(endpoint="accounts.login")
        )
    context = {"title": "Reset password", "form": form}
    return flask.render_template(
        template_name_or_list="accounts/reset_password.html", **context
    )
