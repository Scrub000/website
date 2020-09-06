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

import types
from http import client as http_client
from typing import Optional

import flask
import pytest
from flask import testing, wrappers
from lxml import html

import website
from tests import factories
from website import db


class Response(wrappers.Response):
    """
    Enhanced `Response` class to make testing in Flask easier. Includes
    optional forms in the response, and has assertins for status codes.
    """

    @property
    def forms(self):
        parsed_html = html.document_fromstring(html=self.data)
        forms = parsed_html.forms

        def _submit(
            self,
            follow_redirects: bool = True,
            path: Optional[str] = None,
            method: Optional[str] = None,
            form_data: Optional[dict] = None,
        ):
            data = dict(self.form_values())
            if form_data:
                data.update(form_data)
            if not path:
                path = flask.request.path
            if not method:
                method = self.method
            with flask.current_app.test_client() as test_client:
                if flask.request.cookies.get("session"):
                    # If there is a session, we need to set the session cookie
                    # so that the form submit button will remain authenticated
                    server_name = test_client.application.config["SERVER_NAME"]
                    session = flask.request.cookies["session"]
                    test_client.set_cookie(
                        server_name=server_name, key="session", value=session,
                    )
                return test_client.open(
                    follow_redirects=follow_redirects,
                    path=path,
                    method=method,
                    data=data,
                )

        for form in forms:
            setattr(form, "submit", types.MethodType(_submit, form))
        return forms

    @property
    def form(self):
        forms = self.forms
        if len(forms) >= 1:
            return forms[0]

    def assert_status_ok(self):
        assert self.status_code == http_client.OK

    def assert_status_forbidden(self):
        assert self.status_code == http_client.FORBIDDEN

    def assert_status_found(self):
        assert self.status_code == http_client.FOUND

    def assert_status_not_found(self):
        assert self.status_code == http_client.NOT_FOUND


class FlaskClient(testing.FlaskClient):
    def __init__(self, *args, **kwargs):
        super(FlaskClient, self).__init__(*args, **kwargs)
        self.response_wrapper = Response

    def register(self, username: str, email: str, password: str):
        return self.post(
            path=flask.url_for(endpoint="accounts.register"),
            data=dict(username=username, email=email, password=password),
            follow_redirects=True,
        )

    def request_reset_account_password(self, email: str):
        return self.post(
            path=flask.url_for(endpoint="accounts.request_reset_password"),
            data=dict(email=email),
            follow_redirects=True,
        )

    def reset_account_password(
        self,
        token: str,
        password: str,
        confirm_password: Optional[str] = None,
    ):
        if not confirmed_password:
            confirmed_password = password
        return self.post(
            path=flask.url_for(
                endpoint="accounts.reset_password", token=token
            ),
            data=dict(password=password, confirm_password=confirmed_password),
            follow_redirects=True,
        )


@pytest.fixture(scope="function")
def anon_client():
    """
    Masquerade as an anonymous client.
    """
    app = website.create_app(config_name="Test")
    app.test_client_class = FlaskClient
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
            db.drop_all()


@pytest.fixture(scope="function")
def auth_client(anon_client, factory):
    """
    Masquerade as an unconfirmed account.
    """
    account = factory.Account()
    with anon_client.session_transaction() as session_transaction:
        session_transaction["user_id"] = account.id
        session_transaction["_fresh"] = True
    yield anon_client


@pytest.fixture(scope="function")
def confirmed_auth_client(anon_client, factory):
    """
    Masquerade as a confirmed account.
    """
    account = factory.Account(confirmed=True)
    with anon_client.session_transaction() as session_transaction:
        session_transaction["user_id"] = account.id
        session_transaction["_fresh"] = True
    yield anon_client


@pytest.fixture()
def factory():
    """
    Fixture which returns the 'factories' module.
    """
    return factories
