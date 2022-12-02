from flask import request
from flask_restx import Resource, abort
from flask_restx._http import HTTPStatus

from overseer.api.auth.rbac import AdminOrLeaderOrOwner, Admin
from overseer.api.auth.roles import Role
from overseer.api.flask_restx import api
from overseer.api.auth.auth_model import login_input, login_model, token_header_parser, role_model, role_input
from overseer.api.auth.authentication_service import AuthenticationService
from overseer.api.auth.authorization_service import AuthorizationService
from overseer.api.recordings.recordings_service import RecordingsService
from overseer.api.users.user_service import UserService
from overseer.api.helpers.RequestValidityHandler import RequestValidityHandler

ns = api.namespace('users')


@ns.route('/<id>/role')
class UserRecording(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authorization_service = AuthorizationService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(role_model, code=[HTTPStatus.NO_CONTENT.value, HTTPStatus.UNAUTHORIZED.value,
                                       HTTPStatus.NOT_FOUND.value, HTTPStatus.FORBIDDEN.value, HTTPStatus.BAD_REQUEST.value])
    @ns.expect(role_input)
    def put(self, id):
        role = Role[role_input.parse_args(request)['role']]

        self.request_validity_handler.check_user_authorization(Admin())
        self.request_validity_handler.check_if_valid_id(id)
        self.request_validity_handler.check_user_existence(id)
        self.authorization_service.change_role(id, role)

        return {'result': 'Role changed'}, HTTPStatus.NO_CONTENT
