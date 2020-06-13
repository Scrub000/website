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
from unittest import mock

import flask
import flask_mail

from website.comms import dispatch
from website.domain.accounts import utils


class TestSendConfirmAccountEmail:
    @mock.patch.object(
        target=flask,
        attribute="current_app",
        new=mock.Mock(config={"MAIL_SENDER": "gough.whitlam@alp.org.au"}),
    )
    @mock.patch.object(target=flask, attribute="render_template")
    @mock.patch.object(target=dispatch, attribute="_send_email")
    @mock.patch.object(target=utils, attribute="get_confirm_email_token")
    def test_confirm_account_email_sent(
        self,
        mock_get_confirm_email_token,
        mock_send_email,
        mock_render_template,
    ):
        # ARRANGE
        text_template = "emails/confirm_email/confirm_email.txt"
        html_template = "emails/confirm_email/confirm_email.html"
        token = "valid_token"
        website_name = "Website"
        account = mock.Mock(email="jeremy.corbyn@labour.org.uk")
        mock_get_confirm_email_token.return_value = token

        # ACT
        dispatch.send_confirm_account_email(account=account)

        # ASSERT
        mock_render_template.assert_has_calls(
            calls=[
                mock.call(
                    account=account,
                    name=website_name,
                    template_name_or_list=text_template,
                    token=token,
                ),
                mock.call(
                    account=account,
                    name=website_name,
                    template_name_or_list=html_template,
                    token=token,
                ),
            ]
        )
        mock_send_email.assert_called_once_with(
            subject="Confirm your email",
            sender="gough.whitlam@alp.org.au",
            recipients=[account.email],
            text_body=mock.ANY,
            html_body=mock.ANY,
        )


class TestSendResetPasswordEmail:
    @mock.patch.object(
        target=flask,
        attribute="current_app",
        new=mock.Mock(config={"MAIL_SENDER": "gough.whitlam@alp.org.au"}),
    )
    @mock.patch.object(target=flask, attribute="render_template")
    @mock.patch.object(target=dispatch, attribute="_send_email")
    @mock.patch.object(target=utils, attribute="get_reset_password_token")
    def test_reset_password_email_sent(
        self,
        mock_get_reset_password_token,
        mock_send_email,
        mock_render_template,
    ):
        # ARRANGE
        text_template = "emails/reset_password/reset_password.txt"
        html_template = "emails/reset_password/reset_password.html"
        token = "valid_token"
        website_name = "Website"
        account = mock.Mock(email="jeremy.corbyn@labour.org.uk")
        mock_get_reset_password_token.return_value = token

        # ACT
        dispatch.send_reset_password_email(account=account)

        # ASSERT
        mock_render_template.assert_has_calls(
            calls=[
                mock.call(
                    account=account,
                    name=website_name,
                    template_name_or_list=text_template,
                    token=token,
                ),
                mock.call(
                    account=account,
                    name=website_name,
                    template_name_or_list=html_template,
                    token=token,
                ),
            ]
        )
        mock_send_email.assert_called_once_with(
            subject="Reset your password",
            sender="gough.whitlam@alp.org.au",
            recipients=[account.email],
            text_body=mock.ANY,
            html_body=mock.ANY,
        )


class TestSendContactEmail:
    @mock.patch.object(
        target=flask,
        attribute="current_app",
        new=mock.Mock(
            config={
                "CONTACT_ADDRESS": "richard.dinatale@greens.org.au",
                "MAIL_SENDER": "gough.whitlam@alp.org.au",
            }
        ),
    )
    @mock.patch.object(target=flask, attribute="render_template")
    @mock.patch.object(target=dispatch, attribute="_send_email")
    def test_contact_email_sent(
        self, mock_send_email, mock_render_template,
    ):
        # ARRANGE
        text_template = "emails/contact_email/contact_email.txt"
        html_template = "emails/contact_email/contact_email.html"
        email = "jeremy.corbyn@labour.org.uk"
        enquiry = "For the many, not the few."
        body = "It's time"

        # ACT
        dispatch.send_contact_email(email=email, enquiry=enquiry, body=body)

        # ASSERT
        mock_render_template.assert_has_calls(
            calls=[
                mock.call(
                    email=email,
                    enquiry=enquiry,
                    body=body,
                    template_name_or_list=text_template,
                ),
                mock.call(
                    email=email,
                    enquiry=enquiry,
                    body=body,
                    template_name_or_list=html_template,
                ),
            ]
        )
        mock_send_email.assert_called_once_with(
            subject=f"Enquiry: {enquiry}",
            sender="gough.whitlam@alp.org.au",
            recipients=["richard.dinatale@greens.org.au"],
            text_body=mock.ANY,
            html_body=mock.ANY,
        )


class TestSendEmail:
    @mock.patch.object(target=threading, attribute="Thread")
    @mock.patch.object(target=flask_mail, attribute="Message")
    @mock.patch.object(target=dispatch, attribute="_send_async_email")
    @mock.patch.object(target=flask, attribute="current_app", new=mock.Mock())
    def test_send_email_happy_path(
        self, mock_send_async_email, mock_message, mock_thread,
    ):
        # ARRANGE
        message = mock.Mock()
        mock_message.return_value = message

        # ACT
        dispatch._send_email(
            subject="For the many, not the few",
            sender="gough.whitlam@alp.org.au",
            recipients=["jeremy.corbyn@labour.org.uk"],
            text_body="text",
            html_body="text",
        )

        # ASSERT
        mock_message.assert_called_once_with(
            subject="For the many, not the few",
            sender="gough.whitlam@alp.org.au",
            recipients=["jeremy.corbyn@labour.org.uk"],
            body="text",
            html="text",
        )
        mock_thread.assert_called_once_with(
            target=mock_send_async_email, args=(mock.ANY, message)
        )
