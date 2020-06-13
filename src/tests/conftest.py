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

import pytest

import website
from website import db

from . import factories


@pytest.fixture(scope="session")
def app():
    """
    Fixture for creating an instance of a Flask application. The scope is set
    to 'session'.
    """
    return website.create_app(config_name="Test")


@pytest.fixture(scope="function")
def client(app):
    """
    Fixture for creating a Flask testing client with the application context.
    The scope is set to 'function'.
    """
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def database():
    """
    Fixture for creating an empty database. The scope is set to 'function'.
    """
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture()
def factory():
    """
    Fixture which returns the 'factories' module.
    """
    return factories
