"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/characters/', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    result = [character.serialize() for character in characters]

    return jsonify(result), 200


@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):

    character = Character.query.get(id)
    if character is None:
        return jsonify({"msg": "404 no existe"}), 404

    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200


@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):

    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"msg": "404 no existe"}), 404

    return jsonify(planet.serialize()), 200



@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify(result), 200
















# @app.route('/planet/<int:id>', methods=['DELETE'])
# def deletePlanet(id):
#     planet = Planet.query.get(id)

#     if(planet is None):
#         return jsonify({"msg": "no existe para borrar"})

#     db.session.delete(planet)
#     db.session.commit()

#     return jsonify(planet.serialize()), 200



# @app.route('/planet' , methods=['POST'])
# def createPlanet():
#     # deberias poner body.name y body.description
#     new_planet = Planet(name="Venus", description="planeta verde")
#     db.session.add(new_planet)
#     db.session.commit() #enviar datos a la db
#     return jsonify(new_planet.serialize()), 200





# @app.route('/user', methods=['GET'])
# def handle_hello():

#     planets = Planet.query.all()
#     result = [planet.serialize() for planet in planets]
#     return jsonify(result), 200

# BUSCANDO POR ID
# @app.route('/user/<int:id>', methods=['GET'])
# def handle_hello(id):

#     planet = Planet.query.get(id)
#     if planet is None:
#         return jsonify({"msg": "404 no existe"}), 404

#     return jsonify(planet.serialize()), 200

# BUSCANDO POR NOMBRE
# @app.route('/user/', methods=['GET'])
# def handle_hello():
#     # PARA TREAER TODOS
#     # planets = Planet.query.filter_by(name="Tierra").all()
#     # result = [planet.serialize() for planet in planets]
#     # return jsonify(result), 200
#     # PARA TRAER UNO SOLO, O EL PRIMIERO QUE ENCUENTRE:
#     planet = Planet.query.filter_by(name="Tierra").first()

#     return jsonify(planet.serialize()), 200

# @app.route('/parecido/', methods=['GET'])
# def buscar_parecido():
#     planets = Planet.query.filter(Planet.name.like("%Tie%")).all()
#     result = [planet.serialize() for planet in planets]
    
#     return jsonify(result), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
