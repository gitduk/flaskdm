import os
from logging import getLogger
from logging.config import dictConfig
from dotenv import load_dotenv
from flask import Flask

from flaskr.config import CONFIGS
from flaskr.logger import dict_config, logger_name

# config logger
dictConfig(dict_config)
logger = getLogger(logger_name)


def create_app():
    # load dotenv
    flask_dotenv_path = os.path.join(os.path.abspath("."), ".env.flask")
    load_dotenv(flask_dotenv_path)
    mail_dotenv_path = os.path.join(os.path.abspath("."), ".env.mail")
    load_dotenv(mail_dotenv_path)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load configuration
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(CONFIGS[config_name])

    # blueprint
    from flaskr.views.tasker import tasker

    app.register_blueprint(tasker)

    @app.route('/config')
    def show_config():
        conf = dict(app.config)
        for key, value in conf.items():
            if isinstance(value, (str, tuple, list, bool)): continue
            conf[key] = str(value)

        return conf

    return app
