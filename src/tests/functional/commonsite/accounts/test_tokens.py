# #   Website
# #   Copyright © 2019-2020  scrub
# #
# #   This program is free software: you can redistribute it and/or modify
# #   it under the terms of the GNU Affero General Public License as published by
# #   the Free Software Foundation, either version 3 of the License, or
# #   (at your option) any later version.
# #
# #   This program is distributed in the hope that it will be useful,
# #   but WITHOUT ANY WARRANTY; without even the implied warranty of
# #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# #   GNU Affero General Public License for more details.
# #
# #   You should have received a copy of the GNU Affero General Public License
# #   along with this program. If not, see <http://www.gnu.org/licenses/>.

# from unittest import mock

# from website.domain.accounts import utils


# class TestTokens:
#     @mock.patch.object(utils, attribute="verify_confirm_email_token")
#     def test_account_reset_password(
#         mock_verify_confirm_email_token, anon_client, factory
#     ):
#         account = factory.Account()

#         # Our account should not be confirmed if we do not use the correct token
#         mock_verify_confirm_email_token.return_value = None
#         response = client.get(
#             f"/account/confirm-email/invalid-token", follow_redirects=True
#         )
#         assert response.status_code == http_client.OK
#         assert b"Token is either invalid or expired." in response.data
#         assert not account.updated_at
#         assert not account.is_confirmed

#         # Our account should be confirmed if we use the correct token
#         mock_verify_confirm_email_token.return_value = account
#         response = client.get(
#             f"/account/confirm-email/valid-token", follow_redirects=True
#         )
#         assert response.status_code == http_client.OK
#         assert b"Token is either invalid or expired." not in response.data
#         assert b"Email confirmed." in response.data
#         assert account.updated_at.date()
#         assert account.is_confirmed

#     @mock.patch.object(utils, attribute="verify_reset_password_token")
#     def test_account_confirm_email(
#         mock_verify_reset_password_token, client, database, factory
#     ):
#         account = factory.Account()

#         # We should be informed that an email has been sent to our address and be
#         # redirected to the login page
#         request = utils.request_reset_account_password(
#             client=client, email=account.email
#         )
#         assert request.status_code == http_client.OK
#         assert b"Reset password email has been sent." in request.data
#         assert b"Forgot your password?" in request.data

#         # We should be informed that we entered incorrect details
#         request = utils.request_reset_account_password(
#             client=client, email="jeremy.corbyn@labour.org.uk"
#         )
#         assert request.status_code == http_client.OK
#         assert b"This email does not exist." in request.data

#         # We should be allowed to enter our new password with the correct token
#         mock_verify_reset_password_token.return_value = account
#         response = utils.reset_account_password(
#             client=client, password="For the many, not the few"
#         )
#         assert response.status_code == http_client.OK
#         assert b"Token is either invalid or expired." not in response.data
#         assert b"Password has been reset." in response.data
#         assert account.updated_at.date()

#         # We should not be allowed to reset passwords with an invalid token but
#         # instead be redirected to the login page
#         mock_verify_reset_password_token.return_value = None
#         response = utils.reset_account_password(
#             client=client, password="For the many, not the few"
#         )
#         assert response.status_code == http_client.OK
#         assert b"Token is either invalid or expired." in response.data
#         assert b"Forgot your password?" in response.data
