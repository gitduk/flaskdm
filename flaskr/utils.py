import json
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
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init database
    # from . import db
    # db.init_app(app)

    # blueprints
    # from . import auth
    # app.register_blueprint(auth.bp)

    return app


def get_data(req):
    content_type = req.headers.get("Content-Type", "")
    if content_type.startswith("application"):
        if content_type == "application/json":
            data = req.data
        elif content_type == "application/x-www-form-urlencoded":
            data = req.form
        else:
            data = None
    else:
        data = json.loads(req.data.decode("utf-8"))

    return data
