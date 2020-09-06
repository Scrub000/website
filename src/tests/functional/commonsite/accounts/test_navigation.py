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


class TestNavigation:
    def test_account_navigation(self, anon_client, factory):
        # Navigate to a non-existing account
        non_existing_account_page = anon_client.get(
            path=flask.url_for(
                endpoint="accounts.display", username="non-existing-username"
            )
        )
        non_existing_account_page.assert_status_not_found()
        assert b"Page not found" in non_existing_account_page.data

        # Navigate to an existing account
        account = factory.Account()
        existing_account_page = anon_client.get(
            path=flask.url_for(
                endpoint="accounts.display", username=account.username
            )
        )
        existing_account_page.assert_status_ok()
        assert account.display.encode("utf-8") in existing_account_page.data
