from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Power(db.Model,SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules =()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='powers')
    heroes=db.relationship('Hero',secondary='hero_powers',back_populates='powers')

    def __repr__(self):
        return f'Power {self.id}, name: {self.name} description: {self.description})'


class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True,nullable=False)
    super_name = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='heroes')
    powers=db.relationship('Power',secondary='hero_powers',back_populates='heroes')

    def __repr__(self):
        return f'(Hero {self.id}, name: {self.name} super_name: {self.super_name})'



class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules =()

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.String, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.String, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero', back_populates='hero_powers')
    powers = db.relationship('Power', back_populates='hero_powers')


    def __repr__(self):
        return f'(HeroPower {self.id}, heroID: {self.hero_id} strength: {self.strength}) powerID: {self.power_id}'



# add any models you may need. 