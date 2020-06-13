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

import os

import invoke

PROJECT_ROOT = os.path.dirname(__file__)
WEBSITE_DIR = "src/website"
ENV_DIR = os.path.join(WEBSITE_DIR, ".env")

FLASK_BASE_APP = f"{WEBSITE_DIR}:create_app('Base')"
FLASK_PROD_APP = "website:create_app('Production')"

DEFAULT_ENV = {
    # Flask settings
    "SECRET_KEY": "Change me",
    "SECURITY_PASSWORD_SALT": "Change me",
    # Flask-Mail settings
    "MAIL_SERVER": "smtp.googlemail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": 1,
    "MAIL_USERNAME": "username@gmail.com",
    "MAIL_PASSWORD": "secret",
    "MAIL_SENDER": "username@gmail.com",
    # Website settings
    "CONTACT_ADDRESS": "contact@gmail.com",
    "SOURCE_LINK": "https://github.com/scrub/website",
}

##############
# Installation
##############


@invoke.task
def install(ctx, force=False, dev=False):
    """
    Install all dependencies.
    """
    clean(ctx)
    create_env_file(ctx, force)
    install_python_deps(ctx, dev)
    install_database(ctx, force)


@invoke.task
def create_env_file(ctx, force=False):
    """
    Create environment file.
    """
    env_file = os.path.join(PROJECT_ROOT, ENV_DIR)

    if not os.path.exists(path=env_file) or force:
        with open(env_file, "w") as f:
            for key, value in DEFAULT_ENV.items():
                f.write(f"{key}={value}\n")
        ctx.run(f"cat {env_file}")


@invoke.task
def install_database(ctx, force=False):
    """
    Create database and run migrations.
    
    Assumes migrations have been initialised and migration files exist.
    """
    # TODO: Check if database exists? We may have multiple databases...
    if force:
        ctx.run('find src -type f -name "*.db" -delete', pty=True)

    ctx.run(f"FLASK_APP={WEBSITE_DIR} flask db upgrade")


@invoke.task
def install_python_deps(ctx, dev=False):
    """
    Install Python dependencies.
    """
    ctx.run("pip install -r requirements.txt")
    if dev:
        ctx.run("pip install -r requirements.dev.txt")


###########
# Launching
###########


@invoke.task
def run(ctx, prod=False):
    """
    Run the Flask application in either Debug or Production mode.
    """
    if prod:
        # TODO: Use Gunicorn with Nginx
        ctx.run(f'gunicorn --chdir src "{FLASK_PROD_APP}"')
    else:
        ctx.run(
            f'FLASK_ENV="development" FLASK_APP="{FLASK_BASE_APP}" flask run'
        )


#############
# Development
#############


@invoke.task
def clean(ctx):
    """
    Remove temporary files.
    """
    ctx.run('find src -type f -name "*.pyc" -delete', pty=True)
    ctx.run('find src -type d -name "__pycache__" -delete', pty=True)
    ctx.run('find src -name ".pytest_cache" -exec rm -r "{}" +;', pty=True)
    ctx.run('find -name ".pytest_cache" -exec rm -r "{}" +;', pty=True)
    ctx.run('find -name ".mypy_cache" -exec rm -r "{}" +;', pty=True)


@invoke.task
def run_debug_mail_server(ctx):
    """
    Run the debugging SMTP server on `localhost:8025`.
    """
    ctx.run("python -m smtpd -n -c DebuggingServer localhost:8025")


#########
# Linting
#########


@invoke.task
def run_python_black_linter(ctx):
    ctx.run("black --version")
    ctx.run(
        "cd src && black --line-length=79 --exclude=migrations/* --check ."
    )


@invoke.task
def run_python_isort_linter(ctx):
    ctx.run("isort --version")
    ctx.run("cd src && isort --skip=migrations --check-only")


@invoke.task
def run_python_flake8_linter(ctx):
    ctx.run("flake8 --version")
    ctx.run("cd src && flake8 --exclude=*/migrations/*")


@invoke.task
def run_python_type_checker(ctx):
    ctx.run("mypy --version")
    ctx.run(
        "cd src && PYTHONPATH=${PYTHONPATH}:${PWD} "
        "mypy "
        '$(find ./website -name "*.py" ! -path "*migrations/*" '
        '! -path "*/\.*")',
    )


#########
# Testing
#########


@invoke.task
def run_unit_tests(ctx):
    path = "tests/unit"
    _run_pytest(ctx, path)


@invoke.task
def run_integration_tests(ctx):
    path = "tests/integration"
    _run_pytest(ctx, path)


@invoke.task
def run_functional_tests(ctx):
    path = "tests/functional"
    _run_pytest(ctx, path)


def _run_pytest(ctx, *paths):
    cmd = "cd src && py.test {paths}".format(paths=" ".join(paths))
    ctx.run(cmd)
