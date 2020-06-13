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

from typing import List, Optional

from website.data.accounts import models
from website.domain import exceptions


def get_account(
    id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> models.Account:
    """
    Determine whether an Account is available via the provided keyword
    arguments.

    Raises:
        - `DoesNotExist` if the Account does not exist.
    Returns:
        - The Account associated to the provided `id`, `username` or `email`.
    """
    filters = []

    if id:
        filters.append(models.Account.id == id)
    if username:
        filters.append(models.Account.username.ilike(other=username))
    if email:
        filters.append(models.Account.email.ilike(other=email))
    account = models.Account.query.filter(*filters).first()

    if not account:
        raise exceptions.DoesNotExist("Account does not exist.")
    return account


def get_accounts(
    admin: Optional[bool] = None, confirmed: Optional[bool] = None
) -> List[models.Account]:
    """
    Get all accounts matching the provided keyword arguments.

    Params:
        `admin` - Whether to return administrator or non-administrator
        accounts.
        `confirmed` - Whether to return confirmed or unconfirmed accounts.

    Returns:
        A list of Accounts.
    """
    filters = []

    if admin is not None:
        filters.append(models.Account.admin == admin)
    if confirmed is not None:
        filters.append(models.Account.confirmed == confirmed)

    accounts = (
        models.Account.query.filter(*filters)
        .order_by(models.Account.created_at.desc())
        .all()
    )

    return accounts


def check_login(email: str, password: str) -> models.Account:
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
