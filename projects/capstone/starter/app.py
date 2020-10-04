#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
sys.path.append(os.getcwd())
db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,authorization,True')
        response.headers.add('Acess-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response
    @app.route('/')
    def index():
        return ("Congrats")
    
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_all_actors(payload):
        try:
            Actors = Actor.query.all()
            Actors = [actor.format() for actor in Actors]
            return (jsonify({'success': True, 'Actors': Actors}), 200)
        except:
            abort(401)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(token):
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return (jsonify({'success': True, 'Movies': movies}), 200)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        try:
            x = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if x is None:
                abort(404)
            x.delete()
            return (jsonify({'success': True, 'actor_id': actor_id}),
                    200)
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, id):
        try:
            x = Movie.query.filter(Movie.id == id).one_or_none()
            if x is None:
                abort(404)
            x.delete()
            return (jsonify({'success': True, 'id': id}), 200)
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(token):
        try:
            body = request.get_json()  # fetch the body data from the request body
            requested_name = body.get('name')
            requested_age = body.get('age')
            requested_gender = body.get('gender')
            if requested_name is None:
                abort(422)
            new_actor = Actor(name=requested_name, age=requested_age,
                              gender=requested_gender)  # add the new data to the table as a new record
            new_actor.insert()
            if body is None:
                abort(422)
            return (jsonify({'success': True, 'id': new_actor.id}), 200)
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(token):
        try:
            body = request.get_json()
            requested_title = body.get('title')
            requested_release_date = body.get('release_date')
            requested_actor_id = body.get('actor_id')
            new_movie = Movie(title=requested_title,
                              release_date=requested_release_date,
                              actor_id=requested_actor_id)  # add the new data to the table as a new record
            new_movie.insert()
            if body is None:
                abort(422)
            return (jsonify({'success': True, 'movies': new_movie.id}),
                    200)
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actors(token, id):
        body = request.get_json()  # fetch the body data from the request body
        to_be_updated_row = Actor.query.filter(Actor.id
                == id).one_or_none()  # See if we have that id is in our Table ?
        if to_be_updated_row is None:
            abort(404)  # id   is Not found , we do not have that record in our table
        requested_name = body.get('name')
        requested_age = body.get('age')
        requested_gender = body.get('gender')
        if requested_name is not None:
            to_be_updated_row.name = requested_name
        if requested_age is not None:
            to_be_updated_row.age = requested_age
        if requested_gender is not None:
            to_be_updated_row.gender = requested_gender
        try:
            to_be_updated_row.update()
        except:
            abort(422)
        actors = Actor.query.filter(Actor.id == id).one_or_none()
        if actors is None:
            abort(404)  # The Record is not found
        return (jsonify({'success': True,
                'Actor': to_be_updated_row.id}), 200)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(token, id):
        body = request.get_json()  # fetch the body data from the request body
        to_be_updated_row_n = Movie.query.filter(Movie.id
                == id).one_or_none()  # See if we have that id is in our Table ?
        if to_be_updated_row_n is None:
            abort(404)  # id   is Not found , we do not have that record in our table

        # add the new data to the table as a new record

        if body.get('title') is not None:
            to_be_updated_row_n.title = body.get('title')
        if body.get('release_date') is not None:
            to_be_updated_row_n.release_date = body.get('release_date')


        try:
            to_be_updated_row_n.update()
        except:
            abort(422)
        return (jsonify({'success': True,
                'Movies': to_be_updated_row_n.id}), 200)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)

    @app.errorhandler(400)
    def badrequest(error):
        return (jsonify({'success': False, 'error': 400,
                'message': 'bad request'}), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                'message': 'resource not found'}), 404)

    @app.errorhandler(401)
    def Unauthorized(error):
        return (jsonify({'success': False, 'error': 401,
                'message': 'Unauthorized'}), 401)

    @app.errorhandler(500)
    def server_error(error):
        return (jsonify({'success': False, 'error': 500,
                'message': 'Internal Server Error'}), 500)

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return (jsonify({'sucess': False,
                'error': response.status_code, 'message': response}),
                response.status_code)

    return app


APP = create_app()

## # # print(APP)

if __name__ == '__main__':
    APP.run(debug=True)
