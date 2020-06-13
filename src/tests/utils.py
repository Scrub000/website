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


def login_account(client, email: str, password: str):
    """
    Send POST request to log into an Account.

    Returns Response object.
    """
    return client.post(
        path="account/login",
        data=dict(email=email, password=password),
        follow_redirects=True,
    )


def logout_account(client):
    """
    Send GET request to log out an Account.

    Returns Response object.
    """
    return client.get(path="/account/logout", follow_redirects=True)


def register_account(
    client,
    username: str,
    email: str,
    password: str,
    confirm_password: str = None,
    remember_me: bool = False,
):
    """
    Send POST request to register an Account.

    Returns Response object.
    """
    return client.post(
        path="account/register",
        data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
            if confirm_password
            else password,
            remember_me=remember_me,
        ),
        follow_redirects=True,
    )


def request_reset_account_password(client, email: str):
    """
    Send POST request to request a password reset for Account.

    Returns Response object.
    """
    return client.post(
        path="account/request-reset-password",
        data=dict(email=email),
        follow_redirects=True,
    )


def reset_account_password(
    client,
    password: str,
    confirm_password: str = None,
    token: str = "invalid token",
):
    """
    Send POST request to reset password for Account.

    Returns Response object.
    """
    return client.post(
        path=f"account/reset-password/{token}",
        data=dict(
            password=password,
            confirm_password=confirm_password
            if confirm_password
            else password,
        ),
        follow_redirects=True,
    )
