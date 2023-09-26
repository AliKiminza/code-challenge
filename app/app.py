#!/usr/bin/env python3

from flask import Flask,jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power,Hero_power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "Index for Superheroes API"

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict ={
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name
        }
        heroes.append(hero_dict)

    response = make_response(
        jsonify(heroes),
        200
    )
    return response

@app.route('/heroes/<int:id>', methods=['GET'])
def get_heroes_by_id (id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    hero_dict = {
        "id" : hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers":[{"id": power.id, "name": power.name, "description": power.description}for power in hero.powers]
    }
    return jsonify(hero_dict)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers= []
    for power in powers :
        power_dict = {
            "id" : power.id,
            "name": power.name,
            "description": power.description,
        }

        powers.append(power_dict)

        response = make_response(
            jsonify(powers), 200
        )
        return response

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def get_powers_by_id(id):
    power = Power.query.get(id)
    if power is None :
        return jsonify({"error": "Power not found"}), 404
    
    if request.method == 'GET':
       power_dict = power.to_dict()

       return jsonify(power_dict)
    
    if request.method == 'PATCH':
        power = Power.query.filter_by(id=id).first()

        for attr in request.form:
            setattr(power,attr,request.form.get(attr))

        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()

        response = make_response(
            jsonify(power_dict), 200
        )    
        return response
        
@app.route('/hero_powers', methods=['GET','POST'])
def post_hero_powers():
    if request.method == 'GET':
      hero_powers = []
      for hero_power in Hero_power.query.all():
          hero_power_dict = hero_power.to_dict()
          hero_powers.append(hero_power_dict)

      response = make_response(
            jsonify(hero_powers), 200
        )  
      return response
    
    elif request.method == 'POST':
        new_hero_power = Hero_power(
            strength=request.form.get("strength"),
            power_id=request.form.get("power_id"),
            hero_id=request.form.get("hero_id"),
        )

        db.session.add(new_hero_power)
        db.session.commit()

        if new_hero_power is None:
         return jsonify({"error": "validation errors"}), 404

        hero_power_dict= {
            "id" : hero_power.id,
            "name": hero_power.name,
            "super_name": hero_power.super_name,
            "powers":[{"id": power.id, "name": power.name, "description": power.description}for power in new_hero_power.powers]
        }

        response = make_response(
            jsonify(hero_power_dict), 201
        )

        return response
      
if __name__ == '__main__':
    app.run(port=5555)
