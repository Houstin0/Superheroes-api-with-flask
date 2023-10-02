from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Power(db.Model,SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules =('-heroes','-hero_powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='powers',overlaps="powers")
    heroes=db.relationship('Hero',secondary='hero_powers',back_populates='powers',overlaps="hero_powers")

    def __repr__(self):
        return f'Power {self.id} | name: {self.name} | description: {self.description})'
    
    @validates('description')
    def checks_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be longer than 20 chars")
        else:
            return description


class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers','powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True,nullable=False)
    super_name = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='heroes',overlaps="heroes")
    powers=db.relationship('Power',secondary='hero_powers',back_populates='heroes',overlaps="hero_powers")

    def __repr__(self):
        return f'(Hero {self.id} | name: {self.name} | super_name: {self.super_name})'



class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules =('-heroes','-powers')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.String, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.String, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero', back_populates='hero_powers',overlaps="heroes,powers")
    powers = db.relationship('Power', back_populates='hero_powers',overlaps="heroes,powers")


    def __repr__(self):
        return f'(HeroPower {self.id} | heroID: {self.hero_id} | strength: {self.strength}) powerID: {self.power_id}'
    
    @validates('strength')
    def checks_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be a value either 'Strong', 'Weak' or 'Average'")
        else:
            return strength



# add any models you may need. 