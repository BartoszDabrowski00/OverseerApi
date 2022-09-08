from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from overseer.api.flask_restx import api
from overseer.api.auth.auth_model import login_input, login_model
from overseer.api.auth.authentication_service import AuthenticationService
from overseer.api.auth.authorization_service import AuthorizationService

ns = api.namespace('login')


@ns.route('/')
class Login(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_service = AuthenticationService()
        self.authorization_service = AuthorizationService()

    @ns.marshal_with(login_model, code=[HTTPStatus.OK.value, HTTPStatus.UNAUTHORIZED.value])
    @ns.expect(login_input)
    def post(self):
        ld = login_input.parse_args(request)

        if any([v is None for v in ld.values()]):
            return {'result': 'BAD REQUEST all the fields must be provided'}, HTTPStatus.BAD_REQUEST

        user_id = self.auth_service.check_if_valid_user(ld["email"], ld["password"])
        if user_id is None:
            return {'result': 'UNAUTHORIZED Invalid email or password'}, HTTPStatus.UNAUTHORIZED

        token = self.authorization_service.generate_user_token(user_id)
        return {'result': token}, HTTPStatus.OK
