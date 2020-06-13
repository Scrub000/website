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

import flask_wtf
import wtforms
from wtforms import validators

from website.data.accounts import models
from website.interfaces.common.forms import validators as custom_validators


class Login(flask_wtf.FlaskForm):
    email = wtforms.StringField(
        label="Email",
        validators=[
            validators.InputRequired(message="Please enter an email address."),
            validators.Email(message="Please enter a valid email address."),
        ],
    )
    password = wtforms.PasswordField(
        label="Password",
        validators=[
            validators.InputRequired(message="Please enter a password.")
        ],
    )
    remember_me = wtforms.BooleanField(label="Remember me", default=False)
    submit = wtforms.SubmitField(label="Submit")


class Register(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        label="Username",
        validators=[
            validators.Regexp(
                regex="^\w+$",  # noqa
                message="Username contains invalid characters.",
            ),
            validators.InputRequired(message="Please enter a username."),
            validators.Length(
                min=4,
                max=64,
                message="Username must between 4 and 64 characters long.",
            ),
            custom_validators.IUnique(
                model=models.Account,
                field=models.Account.username,
                message="This username already exists.",
            ),
        ],
    )
    display = wtforms.StringField(
        label="Display name",
        validators=[
            validators.Length(
                max=100,
                message="Display name must be less than 100 characters long.",
            ),
        ],
    )
    email = wtforms.StringField(
        label="Email",
        validators=[
            validators.InputRequired(message="Please enter an email address."),
            validators.Email(message="Please enter a valid email address."),
            validators.Length(
                min=4,
                max=120,
                message="Email must be between 4 and 120 characters long.",
            ),
            custom_validators.IUnique(
                model=models.Account,
                field=models.Account.email,
                message="This email already exists.",
            ),
        ],
    )
    password = wtforms.PasswordField(
        label="Password",
        validators=[
            validators.InputRequired(message="Please enter your password."),
            validators.Length(
                min=8,
                max=255,
                message="Password must be between 8 and 255 characters long.",
            ),
        ],
    )
    confirm_password = wtforms.PasswordField(
        label="Confirm password",
        validators=[
            validators.InputRequired(message="Please re-enter your password."),
            validators.EqualTo(
                fieldname="password", message="Passwords do not match."
            ),
        ],
    )
    submit = wtforms.SubmitField(label="Submit")


class Edit(flask_wtf.FlaskForm):
    display = wtforms.StringField(
        label="Display name",
        validators=[
            validators.Length(
                max=100,
                message="Display name must be less than 100 characters long.",
            ),
        ],
    )
    about = wtforms.TextAreaField(
        label="About me",
        validators=[
            validators.Length(
                max=300, message="About me must be less than 300 characters."
            )
        ],
    )
    submit = wtforms.SubmitField(label="Submit")


class Delete(flask_wtf.FlaskForm):
    confirm = wtforms.BooleanField(
        label="Are you sure you want to delete this account?",
        validators=[
            validators.InputRequired(
                message="Please confirm that you want to delete this account."
            )
        ],
    )
    delete_blogs = wtforms.BooleanField(label="Delete blogs?")
    submit = wtforms.SubmitField(label="Delete")


class EmailRequest(flask_wtf.FlaskForm):
    email = wtforms.StringField(
        label="Email",
        validators=[
            validators.InputRequired(message="Please enter an email address."),
            validators.Email(message="Please enter a valid email address."),
        ],
    )
    submit = wtforms.SubmitField(label="Send request")


class ResetPassword(flask_wtf.FlaskForm):
    password = wtforms.PasswordField(
        label="Password",
        validators=[
            validators.InputRequired(message="Please enter your password."),
            validators.Length(
                min=8,
                max=255,
                message="Password must be between 8 and 255 characters long.",
            ),
        ],
    )
    confirm_password = wtforms.PasswordField(
        label="Confirm password",
        validators=[
            validators.InputRequired(message="Please re-enter your password."),
            validators.EqualTo(
                fieldname="password", message="Passwords do not match."
            ),
        ],
    )
    submit = wtforms.SubmitField(label="Submit")
