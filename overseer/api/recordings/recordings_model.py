from flask_restx import reqparse, fields
from werkzeug.datastructures import FileStorage

from overseer.api.flask_restx import api

recording_input = reqparse.RequestParser()
recording_input.add_argument('recording', type=FileStorage, required=True, location='files')
recording_input.add_argument('user_id', type=int, required=True)
recording_input.add_argument('timestamp', type=str, required=True)

model = api.model('recording upload reply', {
    'result': fields.String
})
