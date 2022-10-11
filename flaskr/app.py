from flask_mail import Mail
from flask_pymongo import PyMongo

from flaskr import create_app

# create app
app = create_app()

# database client
mongo = PyMongo(app)

# mail client
mail = Mail(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
