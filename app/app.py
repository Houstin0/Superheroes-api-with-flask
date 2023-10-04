#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Resource,Api
import os

from models import db, Hero,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        try:
            response_dict = {
                "index": "Welcome to the Hero RESTful API",
            }
            return make_response(jsonify(response_dict), 200)
            
        except Exception as e:
            response_dict = {"error": "An error occurred."}
            return make_response(jsonify(response_dict), 500)

api.add_resource(Index, '/')

class Heroes(Resource):
    def get(self):
        try:
            heroes=Hero.query.all()
            heroes_dicts=[hero.to_dict() for hero in heroes]
            return make_response(jsonify(heroes_dicts),200)
        
        except Exception as e:
            response_dict = {"error": f"An error occurred while fetching heroes.{str(e)}"}
            return make_response(jsonify(response_dict), 500)
        
api.add_resource(Heroes,'/heroes')   

class HeroByID(Resource):

    
    def get (self,id):
        try:
            hero=Hero.query.filter_by(id=id).first()
            if hero:
                hero_dict=hero.to_dict()
                return make_response(jsonify(hero_dict),200)
            else:
                response_dict = {"error": "Hero not found"}
                return make_response(jsonify(response_dict), 404)

        except Exception as e:
            response_dict = {"error": f"An error occurred while fetching hero by ID.{str(e)}"}
            return make_response(jsonify(response_dict), 500)
        
api.add_resource(HeroByID,'/heroes/<int:id>')   

class Powers(Resource):
    def get(self):
        try:
            powers=Power.query.all()
            powers_dicts=[power.to_dict() for power in powers]
            return make_response(jsonify(powers_dicts),200)
        
        except Exception as e:
            response_dict = {"error": f"An error occurred while fetching powers.{str(e)}"}
            return make_response(jsonify(response_dict), 500)
        
api.add_resource(Powers,'/powers')  

class PowerByID(Resource):
    def get (self,id):
        try:
            power=Power.query.filter_by(id=id).first()
            if power:
                power_dict=power.to_dict()
                return make_response(jsonify(power_dict),200)
            else:
                response_dict = {"error": "Power not found"}
                return make_response(jsonify(response_dict), 404)

        except Exception as e:
            response_dict = {"error": f"An error occurred while fetching power by ID.{str(e)}"}
            return make_response(jsonify(response_dict), 500)
        
    def patch(self,id):
        data = request.get_json()
        try:
            power= Power.query.filter_by(id=id).first()
            if power:
                for attr in data:
                    setattr(power,attr,data.get(attr))
                db.session.add(power)
                db.session.commit()

                response_dict=power.to_dict()
                return make_response(jsonify(response_dict),200)   
            else:
                response_dict = {"error": "Power not found"}
                return make_response(jsonify(response_dict), 404)

            
        except Exception as e:
            response_dict = {"error": f"{str(e)}"}
            return make_response(jsonify(response_dict), 500)    
        
api.add_resource(PowerByID,'/powers/<int:id>')

class HeroPowers(Resource):
    def get(self):
        try:
            hero_powers=HeroPower.query.all()
            hero_powers_dicts=[hero_powers.to_dict() for hero_powers in hero_powers]
            return make_response(jsonify(hero_powers_dicts),200)
            
        
        except Exception as e:
            response_dict = {"error": "An error occurred while fetching hero_powers."}
            return make_response(jsonify(response_dict), 500)

     
    def post(self):
        data = request.get_json()
        try:
            new_hero_powers=HeroPower(
                strength=data.get('strength'),
                power_id= data.get("power_id"),
                hero_id= data.get("hero_id"),
            ) 
            db.session.add(new_hero_powers)
            db.session.commit()
        
            response = make_response(
                new_hero_powers.to_dict(),
                201 
            )
            return response
        
        except Exception as e:
            response_dict = {"error" : f"{str(e)}"}
            return make_response(jsonify(response_dict), 403)

    
api.add_resource(HeroPowers, '/hero_powers')





if __name__ == '__main__':
    app.run(port=5555,debug=True)
