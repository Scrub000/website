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


class TestLogin:
    def test_account_login_happy_path(self, anon_client, factory):
        account = factory.Account(confirmed=True)

        # Navigate to the login page
        login_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.login")
        )
        login_response.assert_status_ok()

        # Fill out the form details
        form = login_response.form
        form.fields["email"] = account.email
        form.fields["password"] = "password"

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # We should be informed that we logged in
        assert (
            b"Logged in as " + account.display.encode("utf-8") + b"."
            in form_response.data
        )

    def test_account_login_fails_when_unconfirmed(self, anon_client, factory):
        account = factory.Account()

        # Navigate to the login page
        login_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.login")
        )
        login_response.assert_status_ok()

        # Fill out the form details
        form = login_response.form
        form.fields["email"] = account.email
        form.fields["password"] = "password"

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # We should be informed that we have not confirmed our email
        assert b"Your email has not been confirmed." in form_response.data

    def test_account_login_fails_when_incorrect_password(
        self, anon_client, factory
    ):
        account = factory.Account(confirmed=True)

        # Navigate to the login page
        login_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.login")
        )
        login_response.assert_status_ok()

        # Fill out the form details
        form = login_response.form
        form.fields["email"] = account.email
        form.fields["password"] = "For the many, not the few!"

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # We should be informed that we entered incorrect login infomation
        assert (
            b"Your email and/or password is incorrect." in form_response.data
        )

    def test_account_login_excludes_authenticated_accounts(
        self, confirmed_auth_client,
    ):
        # Navigate to the login page and follow redirects
        login_response = confirmed_auth_client.get(
            path=flask.url_for(endpoint="accounts.login"),
            follow_redirects=True,
        )
        login_response.assert_status_ok()

        # We should be informed that we cannot view this page
        assert (
            b"Only unauthenticated users can view this page."
            in login_response.data
        )


class TestLogout:
    def test_account_logout_happy_path(self, confirmed_auth_client):
        # Navigate to the logout page and follow redirects
        logout_response = confirmed_auth_client.get(
            path=flask.url_for(endpoint="accounts.logout"),
            follow_redirects=True,
        )
        logout_response.assert_status_ok()

        # We should be informed that we logged out
        assert b"Logged out." in logout_response.data

    def test_account_logout_excludes_anonymous_accounts(self, anon_client):
        # Navigate to the logout page and follow redirects
        logout_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.logout"),
            follow_redirects=True,
        )
        logout_response.assert_status_ok()

        # We should be informed that we need to login
        assert b"Please log in to access this page." in logout_response.data
