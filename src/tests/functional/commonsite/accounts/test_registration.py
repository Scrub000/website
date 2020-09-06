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

from website.data.accounts import models


class TestRegistration:
    def test_account_registration_happy_path(self, anon_client):
        account_details = dict(
            username="gough",
            display="Gough Whitlam",
            email="gough.whitlam@alp.org.au",
            password="It's time",
        )

        # Navigate to the registration page
        registration_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.register")
        )
        registration_response.assert_status_ok()

        # Fill out the form details
        form = registration_response.form
        form.fields["username"] = account_details["username"]
        form.fields["email"] = account_details["email"]
        form.fields["password"] = account_details["password"]
        form.fields["confirm_password"] = account_details["password"]

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()
        assert b"Account registered." in form_response.data

        # There should now be one account created
        assert models.Account.query.count() == 1
        account = models.Account.query.first()
        assert account.username == account_details["username"]
        assert account.display == account_details["username"]
        assert account.email == account_details["email"]
        assert not account.password == account_details["password"]
        assert account.created_at
        assert not account.updated_at

    def test_account_registration_has_existing_details(
        self, anon_client, factory
    ):
        # Create an existing account
        account = factory.Account()

        # Navigate to the registration page
        registration_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.register")
        )
        registration_response.assert_status_ok()

        # Fill out the form details, matching the existing account details
        form = registration_response.form
        form.fields["username"] = account.username
        form.fields["display"] = account.display
        form.fields["email"] = account.email
        form.fields["password"] = "password"
        form.fields["confirm_password"] = "password"

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # There should only be one account
        assert models.Account.query.count() == 1

        # We should be informed that an account already exists
        assert b"This username already exists." in form_response.data
        assert b"This email already exists." in form_response.data

    def test_account_registration_invalid_form_details(self, anon_client):
        # Navigate to the registration page
        registration_response = anon_client.get(
            path=flask.url_for(endpoint="accounts.register")
        )
        registration_response.assert_status_ok()

        # Enter invalid information into the form
        form = registration_response.form
        form.fields["username"] = "Gough Whitlam"
        form.fields["password"] = "password"
        form.fields["confirm_password"] = "Non-matching password"

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # There should be no accounts created
        assert models.Account.query.count() == 0

        # We should be informed that we're missing details, we've entered
        # invalid characters, and that the passwords do not match
        assert b"Username contains invalid characters." in form_response.data
        assert b"Please enter an email address." in form_response.data
        assert b"Passwords do not match." in form_response.data

    def test_account_registration_excludes_authenticated_accounts(
        self, confirmed_auth_client,
    ):
        # Navigate to the register page and follow redirects
        register_response = confirmed_auth_client.get(
            path=flask.url_for(endpoint="accounts.register"),
            follow_redirects=True,
        )
        register_response.assert_status_ok()

        # We should be informed that we cannot view this page
        assert (
            b"Only unauthenticated users can view this page."
            in register_response.data
        )
