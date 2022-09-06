from flask_restx import reqparse, fields

from overseer.api.flask_restx import api

login_input = reqparse.RequestParser()
login_input.add_argument('email', type=str, required=True)
login_input.add_argument('password', type=str, required=True)

login_model = api.model('user registration reply', {
    'result': fields.String
})
