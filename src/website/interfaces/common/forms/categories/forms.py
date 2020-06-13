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

from website.data.categories import models
from website.interfaces.common.forms import validators as custom_validators


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
            custom_validators.IUnique(
                model=models.Category,
                field=models.Category.title,
                message="This title already exists.",
            ),
        ],
    )
    description = wtforms.StringField(
        label="Description",
        validators=[
            validators.InputRequired(
                message="Please write something for this category."
            ),
            validators.Length(
                min=4,
                max=150,
                message=(
                    "Description must be between 4 and 150 characters long."
                ),
            ),
        ],
    )
    submit = wtforms.SubmitField(label="Submit")


class Create(Base):
    pass


class Edit(Base):
    pass


class Delete(flask_wtf.FlaskForm):
    confirm = wtforms.BooleanField(
        label="Are you sure you want to delete this category?",
        validators=[
            validators.InputRequired(
                message="Please confirm that you want to delete this category."
            )
        ],
    )
    submit = wtforms.SubmitField(label="Delete")
