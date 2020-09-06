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


class TestUpdateDetails:
    def test_update_account_details_happy_path(self, confirmed_auth_client):
        account = models.Account.query.first()
        display = "Jeremy Corbyn"
        about = "For the many, not the few!"

        # Navigate to the edit account page
        edit_page = confirmed_auth_client.get(
            path=flask.url_for(
                endpoint="accounts.edit", username=account.username
            )
        )
        edit_page.assert_status_ok()

        # Fill out the form details
        form = edit_page.form
        form.fields["display"] = display
        form.fields["about"] = about

        # Submit the form and follow redirect
        form_response = form.submit()
        form_response.assert_status_ok()

        # We should now have updated details
        assert account.display == display
        assert account.about == about

    def test_update_account_details_fails_when_unconfirmed(self, auth_client):
        account = models.Account.query.first()

        # Navigate to the edit account page
        edit_page = auth_client.get(
            path=flask.url_for(
                endpoint="accounts.edit", username=account.username
            )
        )
        edit_page.assert_status_forbidden()

        # We should be informed that we cannot view this page
        assert (
            b"You do not have permission to view this page." in edit_page.data
        )

    def test_update_account_details_fails_when_different_account(
        self, confirmed_auth_client, factory
    ):
        factory.Account(username="jeremy", email="jeremy.corbyn@labour.co.uk")

        # Navigate to the edit account page
        edit_page = confirmed_auth_client.get(
            path=flask.url_for(endpoint="accounts.edit", username="jeremy")
        )
        edit_page.assert_status_forbidden()

        # We should be informed that we cannot view this page
        assert (
            b"You do not have permission to view this page." in edit_page.data
        )
