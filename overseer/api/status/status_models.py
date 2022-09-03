from flask_restx import fields

from overseer.api.flask_restx import api

model = api.model("status model", {
    'status': fields.String
})
