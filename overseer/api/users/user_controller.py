from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from flask_restx import abort

from overseer.api.auth.authorization_service import AuthorizationService
from overseer.api.flask_restx import api
from overseer.api.users.user_service import UserService
from overseer.api.users.user_model import user_model

ns = api.namespace('users')


@ns.route('/')
class Users(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.authorization_service = AuthorizationService()

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def get(self):
        user_id = self.authorization_service.check_if_authorized(request.headers)
        if user_id is None:
            abort(HTTPStatus.UNAUTHORIZED.value, result='UNAUTHORIZED user me be log in')

        return self.user_service.get_all_users(), HTTPStatus.OK


@ns.route('/current')
class CurrentUser(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.authorization_service = AuthorizationService()

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def get(self):
        user_id = self.authorization_service.check_if_authorized(request.headers)
        if user_id is None:
            abort(HTTPStatus.UNAUTHORIZED.value, result='UNAUTHORIZED user me be log in')

        return self.user_service.get_user(user_id), HTTPStatus.OK


@ns.route('/<id>')
class User(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value])
    def get(self, id):
        user_id = self.authorization_service.check_if_authorized(request.headers)
        if user_id is None:
            abort(HTTPStatus.UNAUTHORIZED.value, result='UNAUTHORIZED user me be log in')

        return self.user_service.get_user(id), HTTPStatus.OK
