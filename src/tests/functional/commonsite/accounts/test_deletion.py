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
import pytest

from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models


class TestDeletion:
    @pytest.mark.parametrize(
        argnames="delete_blogs, blog_count", argvalues=[(True, 0), (False, 1)],
    )
    def test_account_deletion_happy_path(
        self, confirmed_auth_client, factory, delete_blogs, blog_count
    ):
        account = account_models.Account.query.first()
        factory.Blog(author=account)

        # Navigate to the account deletion page
        deletion_response = confirmed_auth_client.get(
            path=flask.url_for(
                endpoint="accounts.delete", username=account.username
            )
        )
        deletion_response.assert_status_ok()

        # Fill out the form details
        form = deletion_response.form
        form.fields["confirm"] = True
        form.fields["delete_blogs"] = delete_blogs

        # Submit the form
        form_response = form.submit(follow_redirects=False)
        form_response.assert_status_found()

        # Ensure that no accounts exist and that the blogs are deleted or kept
        assert account_models.Account.query.count() == 0
        assert blog_models.Blog.query.count() == blog_count
