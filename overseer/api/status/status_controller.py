from flask_restx import Resource
from flask_restx._http import HTTPStatus

from overseer.api.flask_restx import api
from overseer.api.status.status_models import model

ns = api.namespace('status')


@ns.route('/')
class Status(Resource):

    @ns.marshal_with(model, code=HTTPStatus.OK)
    def get(self):
        return {'status': 'running'}, HTTPStatus.OK
