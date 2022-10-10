import os
from flask import Flask
from logging.config import dictConfig

from logger import dict_config


def create_app(test_config=None):
    # config logger
    dictConfig(dict_config)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JSON_AS_ASCII=False,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the config, if it exists, when not testing
        app.config.from_pyfile(os.path.abspath("flaskr/config.py"), silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
