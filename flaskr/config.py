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


class ProductionConfig(Config, FlaskMongoConfig):
    """
    Custom configuration
    """


class DevelopmentConfig(Config, FlaskMongoConfig):
    """
    Custom configuration
    """


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
