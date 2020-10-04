import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer,DateTime

import json

# database_name = "castingagency"
database_path = os.getenv('DATABASE_URL')
# postgresql://postgres:123@localhost:5432/castingagency
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()
'''
                                                    Actors

'''
class Actor(db.Model):    
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    #One to Many RelationShip
    movies = db.relationship('Movie', backref='movie' , cascade='all, delete')

    def __init__(self, name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }

'''
                                            Movies

'''
class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    

    #One to Many RelationShip
    actor_id = db.Column(db.Integer , db.ForeignKey('Actor.id'), nullable=False)
   

    def __init__(self, title ,release_date,actor_id):
        self.title = title
        self.release_date = release_date
        self.actor_id=actor_id


    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date' : self.release_date,
        'actor_id' : self.actor_id
        }

# db.create_all()