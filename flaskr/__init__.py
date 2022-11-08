import os
from logging import getLogger
from dotenv import load_dotenv
from flask import Flask

from logger import init_logger
from flaskr.config import CONFIGS

# config logger
init_logger()
logger = getLogger(__name__)


def create_app():
    # load dotenv
    flask_dotenv_path = os.path.join(os.path.abspath("."), ".env")
    load_dotenv(flask_dotenv_path)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load configuration
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(CONFIGS[config_name])

    # blueprint
    from flaskr.views.tasker import tasker
    from flaskr.views.scrapyd import scrapyd

    app.register_blueprint(tasker)
    app.register_blueprint(scrapyd)

    @app.route('/config')
    def show_config():
        conf = dict(app.config)
        for key, value in conf.items():
            if isinstance(value, (str, tuple, list, bool)): continue
            conf[key] = str(value)

        return conf

    return app
