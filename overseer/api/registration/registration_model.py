from flask_restx import reqparse, fields

from overseer.api.flask_restx import api

registration_input = reqparse.RequestParser()
registration_input.add_argument('email', type=str, required=True)
registration_input.add_argument('name', type=str, required=True)
registration_input.add_argument('surname', type=str, required=True)
registration_input.add_argument('password', type=str, required=True)

model = api.model('user registration reply', {
    'result': fields.String
})