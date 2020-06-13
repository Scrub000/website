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

import time
from typing import Optional

import flask
import jwt

from website.data.accounts import models

CONFIRM_EMAIL_KEY = "confirm_email"
RESET_PASSWORD_KEY = "reset_password"


def get_confirm_email_token(
    account: models.Account, expires_in: int = 600
) -> str:
    """
    Return a confirm email token for the given account. By default, this token
    will expire in 6 minutes.
    """
    return _get_token(
        account=account, key_type=CONFIRM_EMAIL_KEY, expires_in=expires_in
    )


def get_reset_password_token(
    account: models.Account, expires_in: int = 600
) -> str:
    """
    Return a reset password token for the given account. By default, this token
    will expire in 6 minutes.
    """
    return _get_token(
        account=account, key_type=RESET_PASSWORD_KEY, expires_in=expires_in
    )


def verify_confirm_email_token(token: str) -> Optional[models.Account]:
    """
    Verify a reset password token against accounts in the database.

    Returns <Account> if token is correct, or `None` otherwise.
    """
    return _verify_token(token=token, key_type=CONFIRM_EMAIL_KEY)


def verify_reset_password_token(token: str) -> Optional[models.Account]:
    """
    Verify a reset password token against accounts in the database.

    Returns <Account> if token is correct, or `None` otherwise.
    """
    return _verify_token(token=token, key_type=RESET_PASSWORD_KEY)


def _verify_token(token: str, key_type: str) -> Optional[models.Account]:
    try:
        pk = jwt.decode(
            jwt=token,
            key=flask.current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
        )[key_type]
    except Exception:
        return None
    else:
        return models.Account.query.get(pk)


def _get_token(
    account: models.Account, key_type: str, expires_in: int = 600,
) -> str:
    return jwt.encode(
        payload={key_type: account.id, "exp": time.time() + expires_in},
        key=flask.current_app.config["SECRET_KEY"],
    ).decode(encoding="utf-8")
