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

from http import client as http_client
from unittest import mock

from tests import utils
from website.data.accounts import models
from website.domain.accounts import utils as account_utils


def test_account_display(client, database, factory):
    factory.Account(about="It's time!")

    # We should see the account's about message on their display page
    response = client.get(path="/account/GOUGH")
    assert response.status_code == http_client.OK
    assert b"It&#39;s time!" in response.data

    # We should receive a 404 status when searching for missing accounts
    response = client.get(path="/account/unknown")
    assert response.status_code == http_client.NOT_FOUND


def test_account_login_and_logout(client, database, factory):
    factory.Account(confirmed=True)
    factory.Account(
        username="Richard", email="richard.dinatale@greens.org.au",
    )
    # We should be successfully logged in and redirected to the landing
    # page
    response = utils.login_account(
        client=client, email="gough.whitlam@alp.org.au", password="It's time"
    )
    assert response.status_code == http_client.OK
    assert b"Logged in as" in response.data

    # We should be redirected back to the landing page as we're already logged
    # in
    response = client.get("account/login", follow_redirects=True)
    assert response.status_code == http_client.OK
    assert b"Only unauthenticated users can view this page." in response.data
    assert b"Forgot your password?" not in response.data

    # We should be logged out
    response = utils.logout_account(client)
    assert response.status_code == http_client.OK
    assert b"Logged in as" not in response.data

    # We should be informed that we entered incorrect details
    response = utils.login_account(
        client=client,
        email="jeremy.corbyn@labour.org.uk",
        password="For the many, not the few",
    )
    assert response.status_code == http_client.OK
    assert b"email and/or password is incorrect" in response.data

    # We should be informed that we have not confirmed our email
    response = utils.login_account(
        client=client,
        email="richard.dinatale@greens.org.au",
        password="It's time",
    )
    assert response.status_code == http_client.OK
    assert b"email has not been confirmed" in response.data


def test_account_registration(client, database):
    # We should have been registered and redirected to the login page
    response = utils.register_account(
        client=client,
        username="Jeremy",
        email="jeremy.corbyn@labour.org.uk",
        password="For the many, not the few",
    )
    account = models.Account.query.filter_by(
        username="Jeremy", email="jeremy.corbyn@labour.org.uk"
    ).first()
    assert response.status_code == http_client.OK
    assert (
        b"Account registered. Please check your email to confirm your account."
        in response.data
    )
    assert b"Forgot your password?" in response.data
    assert account.username == "Jeremy"
    assert account.created_at.date()

    # We should be informed that we entered existing details
    response = utils.register_account(
        client=client,
        username="Jeremy",
        email="jeremy.corbyn@labour.org.uk",
        password="For the many, not the few",
    )
    assert response.status_code == http_client.OK
    assert b"This username already exists" in response.data
    assert b"This email already exists" in response.data
    assert models.Account.query.count() == 1

    # We should be informed that we entered incorrect details
    response = utils.register_account(
        client=client,
        username="Richard Di Natale",
        email=(
            "richard.dinataleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@greens.org.au"
        ),
        password="For the many, not the few",
        confirm_password="A future for all of us",
    )
    assert b"Username contains invalid characters." in response.data
    assert b"Email must be between 4 and 120 characters long." in response.data
    assert b"Passwords do not match." in response.data
    assert models.Account.query.count() == 1


@mock.patch.object(account_utils, attribute="verify_confirm_email_token")
def test_account_reset_password(
    mock_verify_confirm_email_token, client, database, factory
):
    account = factory.Account()

    # Our account should not be confirmed if we do not use the correct token
    mock_verify_confirm_email_token.return_value = None
    response = client.get(
        f"/account/confirm-email/invalid-token", follow_redirects=True
    )
    assert response.status_code == http_client.OK
    assert b"Token is either invalid or expired." in response.data
    assert not account.updated_at
    assert not account.is_confirmed

    # Our account should be confirmed if we use the correct token
    mock_verify_confirm_email_token.return_value = account
    response = client.get(
        f"/account/confirm-email/valid-token", follow_redirects=True
    )
    assert response.status_code == http_client.OK
    assert b"Token is either invalid or expired." not in response.data
    assert b"Email confirmed." in response.data
    assert account.updated_at.date()
    assert account.is_confirmed


@mock.patch.object(account_utils, attribute="verify_reset_password_token")
def test_account_confirm_email(
    mock_verify_reset_password_token, client, database, factory
):
    account = factory.Account()

    # We should be informed that an email has been sent to our address and be
    # redirected to the login page
    request = utils.request_reset_account_password(
        client=client, email=account.email
    )
    assert request.status_code == http_client.OK
    assert b"Reset password email has been sent." in request.data
    assert b"Forgot your password?" in request.data

    # We should be informed that we entered incorrect details
    request = utils.request_reset_account_password(
        client=client, email="jeremy.corbyn@labour.org.uk"
    )
    assert request.status_code == http_client.OK
    assert b"This email does not exist." in request.data

    # We should be allowed to enter our new password with the correct token
    mock_verify_reset_password_token.return_value = account
    response = utils.reset_account_password(
        client=client, password="For the many, not the few"
    )
    assert response.status_code == http_client.OK
    assert b"Token is either invalid or expired." not in response.data
    assert b"Password has been reset." in response.data
    assert account.updated_at.date()

    # We should not be allowed to reset passwords with an invalid token but
    # instead be redirected to the login page
    mock_verify_reset_password_token.return_value = None
    response = utils.reset_account_password(
        client=client, password="For the many, not the few"
    )
    assert response.status_code == http_client.OK
    assert b"Token is either invalid or expired." in response.data
    assert b"Forgot your password?" in response.data
