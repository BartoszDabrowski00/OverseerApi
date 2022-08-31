from flask import Flask

from overseer.api.flask_restx import blueprint
from overseer.utils.config.config import cfg

app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    server_port = cfg.get("server", "port")
    app.run(debug=True, port=server_port)
