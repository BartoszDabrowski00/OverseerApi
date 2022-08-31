from flask_restx import Resource, Namespace

status_namespace = Namespace('status')


@status_namespace.route('/')
class Status(Resource):

    def get(self):
        return {"status": "running"}
