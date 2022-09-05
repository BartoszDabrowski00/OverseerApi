import re
from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from overseer.api.registration.registration_model import model, registration_input
from overseer.api.flask_restx import api
from overseer.api.registration.registration_service import RegistrationService

ns = api.namespace('register')
email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


@ns.route('/')
class Register(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService()

    @ns.marshal_with(model, code=[HTTPStatus.CREATED.value, HTTPStatus.BAD_REQUEST.value, HTTPStatus.CONFLICT.value])
    @ns.expect(registration_input)
    def post(self):
        rd = registration_input.parse_args(request)

        if any([v is None for v in rd.values()]):
            return {'result': 'BAD REQUEST all the fields must be provided'}, HTTPStatus.BAD_REQUEST

        if not re.fullmatch(email_regex, rd["email"]):
            return {'result': 'BAD REQUEST email must be valid'}, HTTPStatus.BAD_REQUEST

        if not self.registration_service.register(rd["email"], rd["name"], rd["surname"], rd["password"]):
            return {'result': 'BAD REQUEST given email is already taken'}, HTTPStatus.CONFLICT



        return {}
