from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'hero'

    serialize_rules = ('-powers.hero')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate= db.func.now())

    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes')
    

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-hero.powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', secondary='hero_powers', back_populates='powers')

    @validates ('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be atleast 20 characters long.")
        return value

class Hero_power(db.Model, SerializerMixin):
    __tablename__ = 'hero-powers'

    id = db.Column(db.Integer,primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers"))

    @ validates('strength') 
    def validate_strength (self, strength, word):
        word = ('Strong', 'weak', 'Average')
        if word not in strength :
            raise ValueError ("failed strength validation")
        return strength
     