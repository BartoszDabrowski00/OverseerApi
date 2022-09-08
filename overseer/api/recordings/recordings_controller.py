from flask import request
from flask_restx import Resource, abort
from flask_restx._http import HTTPStatus

from overseer.api.flask_restx import api
from overseer.api.helpers.RequestValidityHandler import RequestValidityHandler
from overseer.api.recordings.recordings_service import RecordingsService
from overseer.api.recordings.recordings_model import recording_input, model, recording_model
from overseer.api.auth.auth_model import token_header_parser

ns = api.namespace('recordings')


@ns.route('/new_recording')
class Recordings(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recordings_service = RecordingsService()

    @ns.marshal_with(model, code=[HTTPStatus.OK.value, HTTPStatus.BAD_REQUEST.value])
    @ns.expect(recording_input)
    def post(self):
        file = request.files.get('recording', None)
        user_id = request.args.get("user_id", None)
        timestamp = request.args.get('timestamp', None)

        if any(elem is None for elem in [file, user_id, timestamp]):
            return {'result': 'BAD REQUEST All of file, user_id and timestamp fields must be provided'}, HTTPStatus.BAD_REQUEST

        self.recordings_service.send_recording_to_model(file, user_id, timestamp)

        return {'result': 'success'}, HTTPStatus.OK


@ns.route('/all')
class AllRecordings(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recordings_service = RecordingsService()
        self.request_validity_handler = RequestValidityHandler

    @ns.marshal_with(recording_model, code=[HTTPStatus.OK.value, HTTPStatus.UNAUTHORIZED.value])
    @ns.expect(token_header_parser)
    def get(self):
        self.request_validity_handler.check_user_authorization()
        recordings = self.recordings_service.get_all_recordings()
        if len(recordings) == 0:
            abort(404, result="NOT FOUND there are no recordings stored in database")

        return recordings, HTTPStatus.OK
