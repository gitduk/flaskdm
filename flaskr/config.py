import os


class Config:
    """
    Flask configuration
    """
    SECRET_KEY = 'dev',
    JSON_AS_ASCII = False


class FlaskMongoConfig:
    """
    Flask-PyMongo configuration
    """
    MONGO_URI = "mongodb://localhost:27017/flaskr"


class FlaskMailConfig:
    """
    Flask-Mail configuration
    """
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


class ProductionConfig(Config, FlaskMongoConfig, FlaskMailConfig):
    """
    Custom configuration
    """


class DevelopmentConfig(Config, FlaskMongoConfig, FlaskMailConfig):
    """
    Custom configuration
    """


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
