from flask_restx import reqparse, fields
from werkzeug.datastructures import FileStorage

from overseer.api.flask_restx import api


class RecordingFeatures(fields.Raw):
    def format(self, value):
        return value


recording_input = reqparse.RequestParser()
recording_input.add_argument('recording', type=FileStorage, required=True, location='files')
recording_input.add_argument('user_id', type=str, required=True)
recording_input.add_argument('timestamp', type=str, required=True)
recording_input.add_argument('x-access-token', location='headers', required=True)

model = api.model('recording upload reply', {
    'result': fields.String
})

recording_model = api.model('get recording reply', {
            '_id': fields.String,
            'user_id': fields.String,
            'timestamp': fields.String,
            'features': RecordingFeatures
})
