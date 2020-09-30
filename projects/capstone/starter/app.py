import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie 
# from .auth.auth import AuthError, requires_auth

db = SQLAlchemy()
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  # db_drop_and_create_all()
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,authorization,True')
    response.headers.add('Acess-Control-Allow-Methods' , 'GET,POST,PATCH,DELETE,OPTIONS')
    return response
  # db_drop_and_create_all()
  @app.route('/actors')
  def get_all_actors():
    Actors = Actor.query.all()
    Actors = [actor.format() for actor in Actors]
    # a = []
    # for actor in Actors: #actors = [actor-1, actor-2, actor-3]
    #   a.append(actor.formate())
    # Actors = a
    return jsonify ({
      "success" : True,
      "Actors" : Actors
    }),200

  @app.route('/movies')
  def get_all_movies():
    movies= Movie.query.all()
    movies = [ movie.format() for movie in movies]
    return jsonify ({
      "success" : True , 
      "Movies" : movies
    }),200

  @app.route('/actors/<int:actor_id>',methods=['DELETE'])
  def delete_actor(actor_id):

    try:
      x = Actor.query.filter(Actor.id == actor_id).one_or_none()
      # print(x)
      # print(x.format())
      if x is None:
        abort(404)
      x.delete()
      # print(x)
      # print(x.format())
      return jsonify ({
        'success' : True,
        'actor_id' : actor_id
      }),200
    except:
      # db.session.rollback()
      abort(422)
    # finally:
      # db.session.close()

  @app.route('/movies/<int:id>',methods=['DELETE'])
  def delete_movie(id):
    try:
      x=Movie.query.filter(Movie.id == id).one_or_none()
      if x is None:
        abort(404)
    
      x.delete()
      
      return jsonify ({
        "success" : True,
        "id" : id
      }),200
    except:
      abort(422)

  
  @app.route('/actors' , methods=['POST'])
  def  post_actor():
    try:

      #fetch the body data from the request body 
      body = request.get_json()
      requested_name = body.get('name')
      requested_age = body.get('age')
      requested_gender = body.get('gender')
      if  requested_name  is None:
        abort(422)
      #add the new data to the table as a new record
      new_actor = Actor(name=requested_name,age=requested_age,gender=requested_gender)
      new_actor.insert()
      if body is None:
        abort(422)
      return jsonify ({
        "success" : True,
        "id" : new_actor.id
      }),200
    except:
      abort(422)


  @app.route('/movies' , methods=['POST'])
  def  post_movie():

    #fetch the body data from the request body 

    body = request.get_json()
    requested_title = body.get('title')
    requested_release_date = body.get('release_date')
    requested_actor_id = body.get('actor_id')
    #add the new data to the table as a new record
    new_movie = Movie(title=requested_title,release_date=requested_release_date,actor_id=requested_actor_id)
    new_movie.insert()
    if  body   is None:
      abort(422)
    return jsonify ({
      "success" : True,
      "movies" : new_movie.id
    }),200


  @app.route('/actors/<int:id>' , methods =['PATCH'])
  def edit_actors(id):
    #fetch the body data from the request body 
    body = request.get_json()
    requested_name = body.get('name')
    requested_age = body.get('age')
    requested_gender = body.get('gender')
    #add the new data to the table as a new record
    to_be_updated_row = Actor.query.filter(Actor.id == id).one_or_none() #See if we have that id is in our Table ?
    if  to_be_updated_row  is None:
      abort(404) #id   is Not found , we do not have that record in our table
    if ( requested_name or  requested_age or requested_gender ) is None:
      abort(400) # Wrong Input
    to_be_updated_row.name = requested_name
    to_be_updated_row.age = requested_age
    to_be_updated_row.gender = requested_gender
    try:
      to_be_updated_row.update()
    except:
      abort(422)
    actors = Actor.query.filter(Actor.id == id).one_or_none()
    if actors is None:
      abort(404) #The Record is not found
    return jsonify ({
      "success" : True,
      "Actor" : to_be_updated_row.id
    }),200



  @app.route('/movies/<int:id>' , methods =['PATCH'])
  def edit_movies(id):
    #fetch the body data from the request body 
    body = request.get_json()
    requested_title_n = body.get('title')
    requested_release_date_n = body.get('release_date')
    
    #add the new data to the table as a new record
    to_be_updated_row_n=Movie.query.filter(Movie.id == id).one_or_none() #See if we have that id is in our Table ?
    if  to_be_updated_row_n is None:
      abort(404) #id   is Not found , we do not have that record in our table
    if ( requested_title_n or  requested_release_date_n  ) is None:
      abort(400) # Wrong Input
    to_be_updated_row_n.title=requested_title_n
    to_be_updated_row_n.release_date=requested_release_date_n
    # to_be_updated_row_n.actor_id = requested_actor_id_n
    try:
      to_be_updated_row_n.update()
    except:
      abort(422)
    movieys = Movie.query.filter(Movie.id==id).one_or_none()
    if movieys is None:
      abort(404) #The Record is not found
    return jsonify ({
      "success" : True,
      "Movies" : to_be_updated_row_n.id
    }),200

      
  ## Error Handling
  '''
  Example error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404


  @app.errorhandler(401)
  def Unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized"
        }), 401


  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500
    
  # @app.errorhandler(AuthError)
  # def handle_auth_error(ex):
  #   response = jsonify(ex.error)
  #   response.status_code = ex.status_code
  #   return jsonify({
  #       "sucess":False,
  #       "error":response.status_code,
  #       "message" :response
      
  #   }),response.status_code



  return app

APP = create_app()
# # # # print(APP)

if __name__ == '__main__':
    APP.run(debug=True)