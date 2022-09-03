from flask import Blueprint
from flask_restx import Api


blueprint = Blueprint('Overseer API', __name__, url_prefix='/api/overseer/v1')
api = Api(blueprint, version='1.0', title='Overseer API', description='RESTful API for the Overseer project')
