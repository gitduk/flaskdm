import os

# Flask-PyMongo
MONGO_URI = "mongodb://localhost:27017/flaskr"

# flask_mail
MAIL_DEBUG = False
MAIL_SUPPRESS_SEND = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# 自定义配置
BLACK_APP = []
BLACK_TITLE = ["选择输入法", "apolo"]
