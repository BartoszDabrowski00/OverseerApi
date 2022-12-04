import logging

from flask import Flask

from overseer.api.flask_restx import blueprint
from overseer.utils.config.config import Config

log = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(blueprint)
cfg = Config()

if __name__ == '__main__':
    server_port = cfg.get("server", "port")
    host = cfg.get("server", "host")
    logging.basicConfig(level=logging.NOTSET)
    logging.getLogger('pika').setLevel(logging.WARNING)
    log.info(f'Starting on host {host} and port {server_port}')
    app.run(debug=True, host=host, port=server_port)
