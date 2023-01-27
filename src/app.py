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
from models import db, User, Planetas, Favoritos, People, Vehicles
import json
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

@app.route('/user', methods=['GET'])
def handle_user():
    allusers = User.query.all()
    print(allusers)
    results = list(map(lambda item: item.serialize(),allusers))
    print(results)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(results), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def handle_favs(user_id):
    favoritos_usuario = Favoritos.query.filter_by(id = user_id).first()
    favs = favoritos_usuario.serialize()
    # print(allplanetaid)
    
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(favs), 200

@app.route('/people', methods=['GET'])
def handle_people():
    allpeople = People.query.all()
    print(allpeople)
    resultss = list(map(lambda item: item.serialize(),allpeople))
    print(resultss)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(resultss), 200

@app.route('/planetas', methods=['GET'])
def handle_planetas():
    allplanetas = Planetas.query.all()
    print(allplanetas)
    resplanet = list(map(lambda item: item.serialize(),allplanetas))
    print(resplanet)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(resplanet), 200

@app.route('/vlehices', methods=['GET'])
def handle_vehicles():
    allvehicles = Vehicles.query.all()
    print(allvehicles)
    resvehicles = list(map(lambda item: item.serialize(),allvehicles))
    print(resvehicles)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(resvehicles), 200

@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def handle_planetaid(planetas_id):
    allplanetaid = Planetas.query.filter_by(id = planetas_id).first()
    planets = allplanetaid.serialize()
    # print(allplanetaid)
    
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(planets), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_peopleid(people_id):
    allpeopleid = People.query.filter_by(id = people_id).first()
    
    if allpeopleid is None: 
        return jsonify("Persona no existe"), 404
    # print(allpeopleid)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }
    people1 = allpeopleid.serialize()
    return jsonify(people1), 200

@app.route('/user/<int:user_id>/favorite/people', methods=['POST'])
def agregar_people(user_id):
    request_body = request.json #Guardo la respuesta que trae la solicitud en una variable que se llama "request_body" que es un objeto
    print(request_body)
    
    print(request_body["people_id"]) #Accedo a la propiedad "people_id" del objeto "request_body" para obtener su valor
    
    new_favorite_people = Favoritos(planetas_id = None ,usuario_id = user_id, people_id = request_body["people_id"])
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify({"msg":"A sido agregado un nuevo favorito"}), 200



@app.route('/user/<int:user_id>/favorite/planetas', methods=['POST'])
def agregar_planetas(user_id):
    request_body = request.json #Guardo la respuesta que trae la solicitud en una variable que se llama "request_body" que es un objeto
    print(request_body)
    
    print(request_body["planetas_id"]) #Accedo a la propiedad "planetas_id" del objeto "request_body" para obtener su valor
    
    new_favorite_planetas = Favoritos(planetas_id = request_body["planetas_id"] ,usuario_id = user_id, people_id = None)
    db.session.add(new_favorite_planetas)
    db.session.commit()
    return jsonify({"msg":"A sido agregado un nuevo favorito"}), 200

@app.route('/user/<int:user_id>/favorite/planetas', methods=['DELETE'])
def borrar_planetas(user_id):
    request_body = request.json #Guardo la respuesta que trae la solicitud en una variable que se llama "request_body" que es un objeto
    print(request_body)
    
    print(request_body["planetas_id"]) #Accedo a la propiedad "planetas_id" del objeto "request_body" para obtener su valor
    
    # buscar = Favoritos.query.filter_by(usuario_id = user_id, planetas_id = request_body["planetas_id"]).first()
    buscar = Favoritos.query.filter_by(usuario_id = user_id, planetas_id = request_body["planetas_id"]).first()
    db.session.delete(buscar)
    db.session.commit()
    return jsonify({"msg":"A sido eliminado un favorito"}), 200

@app.route('/user/<int:user_id>/favorite/people', methods=['DELETE'])
def borrar_people(user_id):
    request_body = request.json #Guardo la respuesta que trae la solicitud en una variable que se llama "request_body" que es un objeto
    print(request_body)
    
    print(request_body["people_id"]) #Accedo a la propiedad "people_id" del objeto "request_body" para obtener su valor
    
    buscar2 = Favoritos.query.filter_by(usuario_id = user_id, people_id = request_body["people_id"]).first()
    db.session.delete(buscar2)
    db.session.commit()
    return jsonify({"msg":"A sido eliminado un favorito"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
