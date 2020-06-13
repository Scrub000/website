from unittest import mock

import flask_bouncer
from bouncer import models as bouncer_models

from website import authorisation
from website.data.accounts import models as account_models
from website.data.blogs import models as blog_models
from website.data.categories import models as category_models
from website.data.comments import models as comment_models


class TestDefineAuthorisation:
    @mock.patch.object(target=bouncer_models, attribute="RuleList")
    def test_unauthenticated_account_permissions(self, mock_rule_list):
        # ARRANGE
        mock_rule_list = mock.Mock()
        account = mock.Mock(
            is_authenticated=False, is_admin=False, is_confirmed=False
        )

        # ACT
        authorisation.define_authorisation(
            account=account, they=mock_rule_list
        )

        # ASSERT
        assert mock_rule_list.can.call_count == 2
        mock_rule_list.can.assert_has_calls(
            calls=[
                mock.call(
                    action=flask_bouncer.READ,
                    subject=(
                        account_models.Account,
                        category_models.Category,
                        comment_models.Comment,
                    ),
                ),
                mock.call(
                    action=flask_bouncer.READ,
                    subject=blog_models.Blog,
                    published=True,
                ),
            ]
        )

    @mock.patch.object(target=bouncer_models, attribute="RuleList")
    def test_authenticated_account_permissions(self, mock_rule_list):
        # ARRANGE
        mock_rule_list = mock.Mock()
        account = mock.Mock(
            is_authenticated=True, is_admin=False, is_confirmed=False
        )

        # ACT
        authorisation.define_authorisation(
            account=account, they=mock_rule_list
        )

        # ASSERT
        assert mock_rule_list.can.call_count == 2
        mock_rule_list.can.assert_has_calls(
            calls=[
                mock.call(
                    action=flask_bouncer.READ,
                    subject=(
                        account_models.Account,
                        category_models.Category,
                        comment_models.Comment,
                    ),
                ),
                mock.call(
                    action=flask_bouncer.READ,
                    subject=blog_models.Blog,
                    published=True,
                ),
            ]
        )

    @mock.patch.object(target=bouncer_models, attribute="RuleList")
    def test_admin_account_permissions(self, mock_rule_list):
        # ARRANGE
        mock_rule_list = mock.Mock()
        account = mock.Mock(
            is_authenticated=True, is_admin=True, is_confirmed=True
        )

        # ACT
        authorisation.define_authorisation(
            account=account, they=mock_rule_list
        )

        # ASSERT
        assert mock_rule_list.can.call_count == 3
        mock_rule_list.can.assert_has_calls(
            calls=[
                mock.call(
                    action=flask_bouncer.MANAGE, subject=flask_bouncer.ALL,
                )
            ]
        )

    @mock.patch.object(target=bouncer_models, attribute="RuleList")
    def test_confirmed_account_permissions(self, mock_rule_list):
        # ARRANGE
        mock_rule_list = mock.Mock()
        account = mock.Mock(
            is_authenticated=True, is_admin=False, is_confirmed=True
        )

        # ACT
        authorisation.define_authorisation(
            account=account, they=mock_rule_list
        )

        # ASSERT
        assert mock_rule_list.can.call_count == 6
        mock_rule_list.can.assert_has_calls(
            calls=[
                mock.call(
                    action=(
                        flask_bouncer.READ,
                        flask_bouncer.EDIT,
                        flask_bouncer.DELETE,
                    ),
                    subject=account_models.Account,
                    id=account.id,
                ),
                mock.call(
                    action=flask_bouncer.CREATE, subject=blog_models.Blog
                ),
                mock.call(
                    action=(
                        flask_bouncer.READ,
                        flask_bouncer.EDIT,
                        flask_bouncer.DELETE,
                    ),
                    subject=blog_models.Blog,
                    author_id=account.id,
                ),
                mock.call(
                    action=(
                        flask_bouncer.READ,
                        flask_bouncer.EDIT,
                        flask_bouncer.DELETE,
                    ),
                    subject=comment_models.Comment,
                    author_id=account.id,
                ),
            ]
        )
