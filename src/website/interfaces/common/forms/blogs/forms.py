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
from wtforms.ext.sqlalchemy import fields


class Base(flask_wtf.FlaskForm):
    title = wtforms.StringField(
        label="Title",
        validators=[
            validators.InputRequired(message="Please enter a title."),
            validators.Length(
                min=4,
                max=100,
                message="Title must be between 4 and 100 characters long.",
            ),
        ],
    )
    categories = fields.QuerySelectMultipleField(
        label="Categories",
        # TODO: Look into pulling categories from here instead of from the view
        # query_factory=models.Category.query.all(),
        get_label="title",
    )
    description = wtforms.StringField(
        label="Description",
        validators=[
            validators.Length(
                max=150, message="Description exceeds 150 characters."
            ),
        ],
    )
    body = wtforms.TextAreaField(
        label="Body",
        validators=[
            validators.InputRequired(
                message="Please write something for this blog."
            )
        ],
    )
    submit = wtforms.SubmitField(label="Submit")


class Create(Base):
    published = wtforms.BooleanField(label="Publish", default=False)
    comment = wtforms.BooleanField(label="Allow comments", default=True)


class Edit(Base):
    published = wtforms.BooleanField(label="Publish", default=False)
    comment = wtforms.BooleanField(label="Allow comments", default=True)


class Delete(flask_wtf.FlaskForm):
    confirm = wtforms.BooleanField(
        label="Are you sure you want to delete this blog?",
        validators=[
            validators.InputRequired(
                message="Please confirm that you want to delete this blog."
            )
        ],
    )
    submit = wtforms.SubmitField(label="Delete")
