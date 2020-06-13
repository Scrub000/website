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

import flask
import flask_bouncer
import flask_login
import flask_mail
import flask_migrate
import flask_sqlalchemy

CONFIG_LOCATION = "website.settings.config"

# Globally accessible libraries
db = flask_sqlalchemy.SQLAlchemy()
bouncer = flask_bouncer.Bouncer()
login = flask_login.LoginManager()
mail = flask_mail.Mail()
migrate = flask_migrate.Migrate()


class Website(flask.Flask):
    def __init__(self, config_name="Base", name="website", **kwargs):
        # Initialise Flask
        super(Website, self).__init__(import_name=name, **kwargs)

        # Set configuration
        self.config.from_object(obj=f"{CONFIG_LOCATION}.{config_name}")

        # Configure Flask settings
        self.url_map.strict_slashes = self.config["STRICT_SLASHES"]
        self.template_folder = self.config["TEMPLATE_FOLDER"]
        self.static_folder = self.config["STATIC_FOLDER"]

        self.initialise_extensions()
        self.register_blueprints()

    def initialise_extensions(self):
        # Flask-SQLAlchemy
        db.init_app(app=self)

        # Flask-Bouncer
        # Setting authorization_method here to work around the following
        # exception: 'Exception: Expected authorisation method to be set'
        from . import authorisation

        bouncer.init_app(app=self)
        bouncer.user_loader(value=lambda: flask_login.current_user)
        bouncer.authorization_method(value=authorisation.define_authorisation)

        # Flask-Login
        login.init_app(app=self)
        login.login_view = "accounts.login"
        login.login_message = "Please log in to access this page."
        login.login_message_category = "info"

        # Flask-Mail
        mail.init_app(app=self)

        # Flask-Migrate
        migrate.init_app(
            app=self,
            db=db,
            directory=self.config["MIGRATION_FOLDER"],
            # https://alembic.sqlalchemy.org/en/latest/batch.html
            render_as_batch=True,
        )

    def register_blueprints(self):
        # Prevent circular imports
        # See 'Circular Imports' at the bottom of the 'Simple Packages' section
        # https://flask.palletsprojects.com/en/1.1.x/patterns/packages/index.html#simple-packages
        from .interfaces.common.views import views as main_views
        from .interfaces.common.views.accounts import views as account_views
        from .interfaces.common.views.blogs import views as blog_views
        from .interfaces.common.views.categories import views as category_views
        from .interfaces.common.templatetags import filters

        self.register_blueprint(blueprint=main_views.main)
        self.register_blueprint(blueprint=account_views.accounts)
        self.register_blueprint(blueprint=blog_views.blogs)
        self.register_blueprint(blueprint=category_views.categories)
        self.register_blueprint(blueprint=filters.filters)


def create_app(config_name="Base", **kwargs):
    """
    Return a new Flask instance.
    """
    return Website(config_name=config_name, **kwargs)
