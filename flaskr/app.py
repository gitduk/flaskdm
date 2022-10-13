from flask_pymongo import PyMongo

from flaskr import create_app

# create app
app = create_app()

# database client
mongo = PyMongo(app)

if __name__ == '__main__':
    # flask --app=flaskr run --host=0.0.0.0
    app.run(host="0.0.0.0", debug=True)
