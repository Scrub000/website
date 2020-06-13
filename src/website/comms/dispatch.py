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

import threading

import flask
import flask_mail

from website import mail
from website.data.accounts import models
from website.domain.accounts import utils


def send_confirm_account_email(account: models.Account):
    """
    Send a 'confirm email' email to the provided account's email address.
    """
    token = utils.get_confirm_email_token(account=account)
    context = {"name": "Website", "account": account, "token": token}

    _send_email(
        subject="Confirm your email",
        sender=flask.current_app.config["MAIL_SENDER"],
        recipients=[account.email],
        text_body=flask.render_template(
            template_name_or_list="emails/confirm_email/confirm_email.txt",
            **context,
        ),
        html_body=flask.render_template(
            template_name_or_list="emails/confirm_email/confirm_email.html",
            **context,
        ),
    )


def send_reset_password_email(account: models.Account):
    """
    Send a 'reset password' email to the provided account's email address.
    """
    token = utils.get_reset_password_token(account=account)
    context = {"name": "Website", "account": account, "token": token}

    _send_email(
        subject="Reset your password",
        sender=flask.current_app.config["MAIL_SENDER"],
        recipients=[account.email],
        text_body=flask.render_template(
            template_name_or_list="emails/reset_password/reset_password.txt",
            **context,
        ),
        html_body=flask.render_template(
            template_name_or_list="emails/reset_password/reset_password.html",
            **context,
        ),
    )


def send_contact_email(email: str, enquiry: str, body: str):
    """
    Send a contact email to the provided `CONTACT_ADDRESS`.
    """
    context = {"email": email, "enquiry": enquiry, "body": body}
    _send_email(
        subject=f"Enquiry: {enquiry}",
        sender=flask.current_app.config["MAIL_SENDER"],
        recipients=[flask.current_app.config["CONTACT_ADDRESS"]],
        text_body=flask.render_template(
            template_name_or_list="emails/contact_email/contact_email.txt",
            **context,
        ),
        html_body=flask.render_template(
            template_name_or_list="emails/contact_email/contact_email.html",
            **context,
        ),
    )


def _send_email(
    subject: str, sender: str, recipients: list, text_body: str, html_body: str
):
    """
    Send an email asynchronously.
    """
    message = flask_mail.Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body,
    )
    threading.Thread(
        target=_send_async_email,
        args=(flask.current_app._get_current_object(), message),
    ).start()


def _send_async_email(app, message):
    with app.app_context():
        # TODO: Add events
        mail.send(message=message)
