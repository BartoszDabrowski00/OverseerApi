from flask_restx import reqparse, fields

from overseer.api.flask_restx import api

user_model = api.model('user reply', {
    '_id': fields.String,
    'email': fields.String,
    'name': fields.String,
    'surname': fields.String,
})

subordinate_input = reqparse.RequestParser()
subordinate_input.add_argument('x-access-token', location='headers', required=True)
subordinate_input.add_argument('subordinate_id', type=str, required=True, location='form')


