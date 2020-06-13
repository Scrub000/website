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

from ...data.accounts import models
from .. import exceptions


def get_account(username: str = None, email: str = None) -> tuple:
    """
    Determine whether an Account is available via the provided keyword
    arguments.

    Raises:
        - `DoesNotExist` if the Account does not exist.
    Returns:
        - The Account associated to the provided `username` and/or `email`.
    """
    filters = []

    if username:
        filters.append(models.Account.username.ilike(other=username))
    if email:
        filters.append(models.Account.email.ilike(other=email))
    account = models.Account.query.filter(*filters).first()

    if not account:
        raise exceptions.DoesNotExist("Account does not exist.")
    return account


def check_login(email: str, password: str) -> tuple:
    """
    Determine whether the email and password are correct for an Account, and if
    the Account is confirmed.

    Raises:
        - `DoesNotExist` if the Account does not exist.
        - `InvalidPassword` if the Account's password is incorrect.
        - `EmailNotConfirmed` if the Account is not confirmed.
    Returns:
        - The Account associated to the provided `email`.
    """
    account = models.Account.query.filter(
        models.Account.email.ilike(other=email)
    ).first()

    if not account:
        raise exceptions.DoesNotExist("Account does not exist.")
    if not account.check_password(password=password):
        raise exceptions.InvalidPassword("Password is invalid.")
    if not account.is_confirmed:
        raise exceptions.EmailNotConfirmed("Email is not confirmed.")
    return account
