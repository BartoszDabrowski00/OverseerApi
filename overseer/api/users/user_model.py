from flask_restx import reqparse, fields

from overseer.api.flask_restx import api

user_model = api.model('user reply', {
    '_id': fields.String,
    'email': fields.String,
    'name': fields.String,
    'surname': fields.String,
})
