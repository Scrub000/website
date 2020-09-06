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

from website.domain.blogs import queries


class TestHomepage:
    def test_landing_page(self, anon_client, factory):
        # Create an account with some published and unpublished blogs
        account = factory.create_account_with_blogs(
            blog_kwargs=dict(published=True)
        )
        factory.Blog(author=account)
        factory.Blog(author=account)

        # Navigate to the landing page
        landing_response = anon_client.get(
            path=flask.url_for(endpoint="main.landing")
        )
        landing_response.assert_status_ok()

        # Ensure that the published blogs are on the landing page
        for blog in queries.get_blogs(author=account, published=True):
            assert blog.title.encode("utf-8") in landing_response.data
            assert blog.description.encode("utf-8") in landing_response.data
        # Ensure that the unpublished blogs are not on the landing page
        for blog in queries.get_blogs(author=account, published=False):
            assert not blog.title.encode("utf-8") in landing_response.data
            assert (
                not blog.description.encode("utf-8") in landing_response.data
            )
        # Ensure we include the license notice
        assert (
            b"The code of this website is Free Software."
            in landing_response.data
        )

    def test_about_page(self, anon_client):
        # Navigate to the about page
        about_response = anon_client.get(
            path=flask.url_for(endpoint="main.about")
        )
        about_response.assert_status_ok()

        assert b"This is a testing website." in about_response.data
