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

import flask_wtf
import wtforms
from wtforms import validators


class Contact(flask_wtf.FlaskForm):
    email = wtforms.StringField(
        label="Email",
        render_kw={"placeholder": "Email..."},
        validators=[
            validators.InputRequired(message="Please enter an email address."),
            validators.Email(message="Please enter a valid email address."),
        ],
    )
    enquiry = wtforms.StringField(
        label="Enquiry",
        render_kw={"placeholder": "Enquiry..."},
        validators=[
            validators.InputRequired(message="Please fill in your enquiry."),
            validators.Length(
                min=4,
                max=150,
                message="Enquiry must be between 4 and 150 characters long.",
            ),
        ],
    )
    body = wtforms.TextAreaField(
        label="Body",
        render_kw={"placeholder": "Body..."},
        validators=[
            validators.InputRequired(
                message="Please write something for this enquiry."
            )
        ],
    )
    submit = wtforms.SubmitField(label="Submit")
