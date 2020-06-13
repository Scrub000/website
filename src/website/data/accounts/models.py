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

import flask
import flask_login
from sqlalchemy import sql
from werkzeug import security

from website import db, login


class Account(db.Model, flask_login.UserMixin):  # type: ignore
    __tablename__ = "accounts"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    display = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    about = db.Column(db.String(300))

    # Authorisation statuses.
    admin = db.Column(
        db.Boolean(), nullable=False, default=False, server_default="0"
    )
    confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=sql.func.current_timestamp(),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), onupdate=sql.func.current_timestamp()
    )
    seen_at = db.Column(
        db.DateTime(timezone=True), onupdate=sql.func.current_timestamp()
    )

    blogs = db.relationship("Blog", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)

    def __repr__(self):
        return f"<Account {self.username}>"

    @login.user_loader
    def load_account(account_id):
        return Account.query.get(ident=int(account_id))

    @classmethod
    def new(
        cls,
        username: str,
        display: str,
        email: str,
        password: str,
        admin: bool = False,
        confirmed: bool = False,
    ):
        """
        Create a new Account in the database.

        Password is hashed before being saved to the database.

        Returns an Account.
        """
        hashed_password = cls._hash_password(password=password)
        account = cls(
            username=username,
            display=display if display else username,
            email=email,
            password=hashed_password,
            admin=admin,
            confirmed=confirmed,
        )

        db.session.add(account)
        db.session.commit()

        return account

    # Mutators

    def update(self, **kwargs):
        """
        Update Account.
        """
        allowed_attributes = [
            "username",
            "display",
            "email",
            "password",
            "about",
            "admin",
            "confirmed",
            "seen_at",
        ]
        for key, value in kwargs.items():
            assert key in allowed_attributes
            if key == "display":
                if not value:
                    value = self.username
            if key == "password":
                value = Account._hash_password(password=value)
            setattr(self, key, value)
        db.session.commit()

    def delete(self, delete_blogs: bool = False):
        """
        Delete Account.

        Params:
            - `delete_blogs` whether the blogs associated to the Account should
                be deleted. If set to `False`, the blogs will instead be
                transferred to the default Account.
        """
        # TODO: Make this an atomic transaction - i.e. all-or-nothing.
        for blog in self.blogs:
            if delete_blogs:
                blog.delete()
            else:
                blog.update(author=None)
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password: str) -> bool:
        """
        Check the password against saved hashed password.
        """
        return security.check_password_hash(
            pwhash=self.password, password=password
        )

    # Properties

    @property
    def is_admin(self) -> bool:
        return self.admin

    @property
    def is_confirmed(self) -> bool:
        if flask.current_app.config["ACCOUNT_ALWAYS_CONFIRMED"]:
            return True
        return self.confirmed

    # Queries

    # Private

    @classmethod
    def _hash_password(cls, password: str) -> str:
        """
        Return hashed password.
        """
        return security.generate_password_hash(password=password)
