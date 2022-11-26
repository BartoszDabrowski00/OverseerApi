from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from flask_restx import abort

from overseer.api.flask_restx import api
from overseer.api.helpers.RequestValidityHandler import RequestValidityHandler
from overseer.api.recordings.recordings_model import recording_model
from overseer.api.recordings.recordings_service import RecordingsService
from overseer.api.users.user_service import UserService
from overseer.api.users.user_model import user_model, subordinate_input
from overseer.api.auth.auth_model import token_header_parser

ns = api.namespace('users')


@ns.route('/')
@ns.expect(token_header_parser)
class Users(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def get(self):
        self.request_validity_handler.check_user_authorization()
        users = self.user_service.get_all_users()

        if len(users) == 0:
            abort(404, result="NOT FOUND there are no users stored in database")

        return users, HTTPStatus.OK


@ns.route('/current')
@ns.expect(token_header_parser)
class CurrentUser(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def get(self):
        current_user_id = self.request_validity_handler.check_user_authorization()
        user = self.user_service.get_user(current_user_id)
        if user is None:
            abort(404, result="NOT FOUND user does not exist")

        return user, HTTPStatus.OK



@ns.route('/<id>')
@ns.expect(token_header_parser)
class User(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def get(self, id):
        self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id)

        user = self.user_service.get_user(id)
        if user is None:
            abort(404, result='NOT FOUND user does not exist')

        return user, HTTPStatus.OK


@ns.route('/<id>/subordinates')
class Subordinates(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    @ns.expect(token_header_parser)
    def get(self, id):
        self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id)
        self.request_validity_handler.check_user_existence(id)

        subordinates = self.user_service.get_user_subordinates(id)
        if len(subordinates) == 0:
            abort(404, result="NOT FOUND the uer has no subordinates")

        return subordinates, HTTPStatus.OK


    @ns.marshal_with(user_model, code=[HTTPStatus.CREATED.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value, HTTPStatus.BAD_REQUEST.value])
    @ns.expect(subordinate_input)
    def post(self, id):
        subordinate_data = subordinate_input.parse_args(request)
        if subordinate_data['subordinate_id'] is None:
            abort(400, result='BAD REQUEST specify subordinate id.')

        current_id = self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id)
        self.request_validity_handler.check_user_existence(id)

        if current_id != id:
            abort(403, result="User is not allowed to perform this operation.")

        subordinate = self.user_service.get_user(subordinate_data['subordinate_id'])
        if subordinate is None:
            abort(404, result='NOT FOUND subordinate does not exist')

        self.user_service.add_subordinate(id, subordinate_data['subordinate_id'])
        return subordinate, HTTPStatus.CREATED


@ns.route('/<id>/subordinates/<subordinate_id>')
@ns.expect(token_header_parser)
class Subordinate(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(user_model, code=[HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value, HTTPStatus.UNAUTHORIZED.value])
    def delete(self, id, subordinate_id):
        current_id = self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id, subordinate_id)
        self.request_validity_handler.check_user_existence(id)

        if current_id != id:
            abort(403, result="User is not allowed to perform this operation.")

        subordinate = self.user_service.get_user(subordinate_id)

        if subordinate is None:
            abort(404, result='NOT FOUND subordinate does not exist')

        self.user_service.delete_subordinate(id, subordinate_id)

        return subordinate, HTTPStatus.OK


@ns.route('/<id>/recordings')
@ns.expect(token_header_parser)
class UserRecordings(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.recording_service = RecordingsService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(recording_model, code=[HTTPStatus.OK.value, HTTPStatus.UNAUTHORIZED.value, HTTPStatus.NOT_FOUND])
    def get(self, id):
        self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id)
        self.request_validity_handler.check_user_existence(id)

        recordings = self.recording_service.get_user_recordings(id)
        if len(recordings) == 0:
            abort(404, result='The user has no recordings')

        return recordings, HTTPStatus.OK


@ns.route('/<id>/recordings/<recording_id>')
@ns.expect(token_header_parser)
class UserRecording(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.recording_service = RecordingsService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(recording_model, code=[HTTPStatus.OK.value, HTTPStatus.UNAUTHORIZED.value, HTTPStatus.NOT_FOUND])
    def get(self, id, recording_id):
        self.request_validity_handler.check_user_authorization()
        self.request_validity_handler.check_if_valid_id(id, recording_id)
        self.request_validity_handler.check_user_existence(id)

        recording = self.recording_service.get_user_recording(id, recording_id)
        if recording is None:
            abort(404, result="NOT FOUND recording does not exist")

        return recording, HTTPStatus.OK
