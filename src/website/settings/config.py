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

import os

import dotenv_config


class Base:
    """
    Base configuration for Flask website.
    """

    # Root of installed package + website folder
    BASE_DIRECTORY = (
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        + "/website"
    )
    ENV_DIRECTORY = os.path.join(BASE_DIRECTORY, ".env")

    # Load environment variables
    env_config = dotenv_config.Config(path=ENV_DIRECTORY)

    ################
    # Flask settings
    ################
    DEBUG = True
    ENV = "development"
    SECRET_KEY = env_config(name="SECRET_KEY", default="Change me")
    SECURITY_PASSWORD_SALT = env_config(
        name="SECURITY_PASSWORD_SALT", default="Change me"
    )
    STRICT_SLASHES = False
    TEMPLATES_AUTO_RELOAD = True
    TEMPLATE_FOLDER = os.path.join(
        BASE_DIRECTORY, "interfaces/common/templates/"
    )
    STATIC_FOLDER = os.path.join(BASE_DIRECTORY, "interfaces/common/static/")

    #####################
    # SQLAlchemy settings
    #####################
    SQLALCHEMY_DATABASE_URI = env_config(
        name="DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIRECTORY, "database.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #####################
    # Flask-Admin settings
    #####################
    FLASK_ADMIN_SWATCH = env_config(name="FLASK_ADMIN_SWATCH", default="slate")

    ######################
    # Flask-Login settings
    ######################
    REMEMBER_COOKIE_HTTPONLY = True

    #####################
    # Flask-Mail settings
    #####################
    MAIL_SERVER = env_config(name="MAIL_SERVER", default="localhost")
    MAIL_PORT = env_config(name="MAIL_PORT", default=8025, conversion=int)
    MAIL_USE_TLS = env_config(name="MAIL_USE_TLS", conversion=bool)
    MAIL_USERNAME = env_config(name="MAIL_USERNAME")
    MAIL_PASSWORD = env_config(name="MAIL_PASSWORD")
    MAIL_SENDER = env_config(name="MAIL_SENDER")

    ##################
    # Website settings
    ##################
    CONTACT_ADDRESS = env_config(name="CONTACT_ADDRESS")
    SOURCE_LINK = env_config(
        name="SOURCE_LINK", default="https://github.com/scrub/website"
    )
    MIGRATION_FOLDER = "src/website/data/migrations"
    ACCOUNT_ALWAYS_CONFIRMED = True
    FEED_TITLE = env_config(name="FEED_TITLE", default="Feed")
    FEED_DESCRIPTION = env_config(
        name="FEED_DESCRIPTION", default="Simple feed"
    )


class Test(Base):
    """
    Test configuration for unit, integration and functional tests.
    """

    ################
    # Flask settings
    ################
    DEBUG = False
    TESTING = True

    #####################
    # SQLAlchemy settings
    #####################
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    ####################
    # Flask-WTF settings
    ####################
    WTF_CSRF_ENABLED = False

    ##################
    # Website settings
    ##################
    ACCOUNT_ALWAYS_CONFIRMED = False


class Production(Base):
    """
    Production configuration for Flask website.
    """

    ################
    # Flask settings
    ################
    DEBUG = False
    ENV = "production"
    TEMPLATES_AUTO_RELOAD = False
    SESSION_COOKIE_SECURE = True

    ######################
    # Flask-Login settings
    ######################
    REMEMBER_COOKIE_SECURE = True

    ##################
    # Website settings
    ##################
    ACCOUNT_ALWAYS_CONFIRMED = False
