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

from ...comms import dispatch
from ...data.accounts import models
from .. import exceptions


def create_account(
    username: str, display: str, email: str, password: str
) -> models.Account:
    """
    Create an Account in the database.

    Raises:
        - `UnableToCreate` if Account cannot be created.
    Returns:
        - A new Account.
    """
    try:
        account = models.Account.new(
            username=username, display=display, email=email, password=password
        )
    except Exception:
        raise exceptions.UnableToCreate("Unable to create account.")

    # Send comms emails
    dispatch.send_confirm_account_email(account=account)

    # TODO: Publish an event

    return account


def update_account(account: models.Account, **kwargs):
    """
    Update an Account in the database.

    Raises:
        - `UnableToUpdate` if account cannot be updated.
    """
    try:
        account.update(**kwargs)
    except Exception:
        raise exceptions.UnableToUpdate("Unable to update account.")

    # TODO: Send comms emails

    # TODO: Publish an event


def delete_account(account: models.Account, delete_blogs: bool = False):
    """
    Delete an Account from the database.

    Raises:
        - `UnableToDelete` if account cannot be deleted.
    """
    try:
        account.delete(delete_blogs=delete_blogs)
    except Exception:
        raise exceptions.UnableToDelete("Unable to delete account.")

    # TODO: Send comms emails

    # TODO: Publish an event
