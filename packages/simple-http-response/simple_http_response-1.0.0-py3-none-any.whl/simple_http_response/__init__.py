import logging
import re

from flask import Flask

from simple_http_response.config import Config

config = Config()
logging.basicConfig(level=config.LOG_LEVEL)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route(config.ENDPOINT, methods=config.METHOD)
    def index():
        """Serve the index page."""
        _config = Config()
        pattern = re.compile(r'(:\s+|:)')
        headers = {re.split(pattern, header, 1)[0]: re.split(pattern, header, 1)[2] for header in _config.HEADER}
        return _config.BODY, _config.CODE, headers
    return app
