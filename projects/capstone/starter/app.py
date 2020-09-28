import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,authorization,True')
    response.headers.add('Acess-Control-Allow-Methods' , 'GET,POST,PATCH,DELETE,OPTIONS')
    return response

  @app.route('/actors')
  def get_all_actors():
    Actors = Actor.query.all()
    Actors = [Actor.format() for actor in Actors]
    return jsonify ({
      "success" : True,
      "Actors" : Actors
    }),200

  @app.route('/movies')
  def get_all_movies():
    movies= Movie.query.all()
    movies = [ Movie.format() for movie in movies]
    return jsonify ({
      "success" : True , 
      "Movies" : movies
    }),200

  @app.route('/actors/<int:id>' , methods=['DELETE'])
 #@requires_auth('delete:actors')
  def delete_actor(id):
    try:
      x=Actor.query.filter_by(id==id).one_or_none()
      if x is None:
        abort(404)
      try:
        x.delete()
      except:
        abort(422) #Unprocessable Entity
      return ({
        "success" : True,
        "id" : id
      }),200
    except:
      abort(422)

  @app.route('/movie/<int:id>' , methods=['DELETE'])
  #@requires_auth('delete:movie')
  def delete_movie(id):
    try:
      x=Movie.query.filter_by(id==id).one_or_none()
      if x is None:
        abort(404)
      try:
        x.delete()
      except:
        abort(422) #Unprocessable Entity
      return ({
        "success" : True,
        "id" : id
      }),200
    except:
      abort(422)

  
  @app.route('/actors' , methods=['POST'])
  #@requires_auth('post:actors')
  def  post_actor():
    #fetch the body data from the request body 
    body = request.get_json()
    requested_name = body.get('name')
    requested_age = body.get('age')
    requested_gender = body.get('gender')
    #add the new data to the table as a new record
    Actor(name=requested_name,age=requested_age,gender=requested_gender).insert()
    if body is None:
      abort(422)
    return jsonify ({
      "success" : True,
      "actors" : [Actor.format()]
    }),200
  @app.route('/movies' , methods=['POST'])
  #@requires_auth('post:movies')
  def  post_actor():

    #fetch the body data from the request body 

    body = request.get_json()
    requested_title = body.get('title')
    requested_release_date = body.get('release_date')

    #add the new data to the table as a new record
    Movie(title=requested_title,release_date=requested_release_date).insert()
    if body is None:
      abort(422)
    return jsonify ({
      "success" : True,
      "movies" : [Movie.format()]
    }),200


  @app.route('/actors/<int:id>' , methods =['PATCH'])
  #@requires_auth('patch:actors')
  def edit_actors(id):
    #fetch the body data from the request body 
    body = request.get_json()
    requested_name = body.get('name')
    requested_age = body.get('age')
    requested_gender = body.get('gender')
    #add the new data to the table as a new record
    to_be_updated_row=Actor.query.filter_by(Actor.id==id).one_or_none() #See if we have that id is in our Table ?
    if  to_be_updated_row  is None:
      abort(404) #id   is Not found , we do not have that record in our table
    if ( requested_name or  requested_age or requested_gender ) is None:
      abort(400) # Wrong Input
    to_be_updated_row.name=requested_name
    to_be_updated_row.age=requested_age
    to_be_updated_row.gender=requested_gender
    try:
      to_be_updated_row.update()
    except:
      abort(422)
    actors = Actor.query.filter_by(Actor.id==id).one_or_none()
    if actors is None:
      abort(404) #The Record is not found
    return jsonify ({
      "success" : True,
      "Actors" : [Actor.format()]
    }),200



  @app.route('/movies/<int:id>' , methods =['PATCH'])
  #@requires_auth('patch:movies')
  def edit_movies(id):
    #fetch the body data from the request body 
    body = request.get_json()
    requested_title = body.get('title')
    requested_release_date = body.get('release_date')
  
    #add the new data to the table as a new record
    to_be_updated_row=Movie.query.filter_by(Movie.id==id).one_or_none() #See if we have that id is in our Table ?
    if  to_be_updated_row  is None:
      abort(404) #id   is Not found , we do not have that record in our table
    if ( requested_title or  requested_release_date  ) is None:
      abort(400) # Wrong Input
    to_be_updated_row.name=requested_title
    to_be_updated_row.age=requested_release_date

    try:
      to_be_updated_row.update()
    except:
      abort(422)
    movies = Movie.query.filter_by(Movie.id==id).one_or_none()
    if movies is None:
      abort(404) #The Record is not found
    return jsonify ({
      "success" : True,
      "Movies" : [Movie.format()]
    }),200


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)