from flask import Flask
from flask_restful import Api
from os import environ
from flask_jwt import JWT

# sajat fajlok
from resources.car import CarList, Car
from resources.driver import Driver
from resources.user import UserRegister
from resources.assign import AssignDriverToCar
from db import db

from security import authenticate, identity

# példányosítjuk a Flusk-ot és configuráljuk
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
# ez kell a user auth-hoz
app.secret_key = environ.get('SECRET_KEY')

api = Api(app)

# ezzel kötjük össze az Alchemy-t a Flask-kal
db.init_app(app)

# authentikáció
jwt = JWT(app, authenticate, identity)

# special route in Flask - mielőtt az első req érkezne a severhez
@app.before_first_request
def create_tables():
  # db-t hozza létre és a táblákat üresen, sql db-t
  db.create_all()


api.add_resource(CarList, '/cars')
api.add_resource(Car, '/cars/<string:plate>')
api.add_resource(UserRegister, '/register')
api.add_resource(Driver, '/driver')
api.add_resource(AssignDriverToCar, '/assign')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)