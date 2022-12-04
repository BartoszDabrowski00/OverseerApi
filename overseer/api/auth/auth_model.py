from flask_restx import reqparse, fields

from overseer.api.auth.roles import Role
from overseer.api.flask_restx import api

login_input = reqparse.RequestParser()
login_input.add_argument('email', type=str, required=True, location='form')
login_input.add_argument('password', type=str, required=True, location='form')

role_input = reqparse.RequestParser()
role_input.add_argument('role', choices=(Role._member_names_), required=True, location='form')
role_input.add_argument('x-access-token', location='headers', required=True)

token_header_parser = api.parser()
token_header_parser.add_argument('x-access-token', location='headers', required=True)

login_model = api.model('user registration reply', {
    'result': fields.String
})

role_model = api.model('role change reply', {
    'result': fields.String
})
