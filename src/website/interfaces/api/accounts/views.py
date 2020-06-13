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

import http

import flask
import flask_bouncer
import flask_restx
from flask import request
from flask_restx import fields

from website import decorators
from website.domain.accounts import operations, queries
from website.interfaces import api
from website.interfaces.api.accounts import serializers

accounts = flask.Blueprint(
    name="api-accounts", import_name=__name__, url_prefix="/api/v1/accounts",
)
api_accounts = api.Api(
    app=accounts,
    version="1.0",
    title="Accounts API",
    description="API for accounts, which currently relies on session cookies.",
)
account_marshaller = api_accounts.model(
    name="Account", model=dict(display=fields.String, about=fields.String),
)


class AccountDetail(flask_restx.Resource):
    serializer = serializers.Account()

    def get(self, id: int):
        account = queries.get_account(id=id)
        return self.serializer.dump(obj=account), http.HTTPStatus.OK

    @decorators.api_login_required
    @api_accounts.expect(account_marshaller)
    def put(self, id: int):
        account = queries.get_account(id=id)
        flask_bouncer.ensure(action=flask_bouncer.EDIT, subject=account)
        payload = request.get_json(force=True)
        data = self.serializer.load(data=payload)
        operations.update_account(account=account, **data)
        return self.serializer.dump(obj=account), http.HTTPStatus.ACCEPTED


class AccountList(flask_restx.Resource):
    serializer = serializers.Account()

    def get(self):
        accounts = queries.get_accounts()
        return (
            self.serializer.dump(obj=accounts, many=True),
            http.HTTPStatus.OK,
        )


api_accounts.add_resource(AccountDetail, "/<int:id>")
api_accounts.add_resource(AccountList, "/list")
