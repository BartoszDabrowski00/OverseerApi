from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from overseer.api.flask_restx import api
from overseer.api.recordings.recordings_service import RecordingsService
from overseer.api.recordings.recordings_model import recording_input, model

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
