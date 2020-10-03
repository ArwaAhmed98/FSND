#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'castingagency'
        self.database_path = \
            'postgresql://postgres:123@localhost:5432/castingagency'
        setup_db(self.app)

        # binds the app to the current context

        with self.app.app_context():

            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables

            self.db.create_all()

            # give the attribuites of the class any values

            self.new_actor = {'name': 'Nada', 'age': 20,
                              'gender': 'Female'}

        self.assistant_token = 'Bearer ' + os.getenv('Assistant')

        self.director_token = 'Bearer ' + os.getenv('director')

        self.producer_token = 'Bearer ' + os.getenv('producer')

        self.assistant_header = {'Authorization': self.assistant_token}

        self.director_header = {'Authorization': self.director_token}
        self.producer_header = {'Authorization': self.producer_token}

    def tearDown(self):
        """Executed after reach test"""

        pass

    def test_get_all_actors(self):

        res = self.client().get('/actors',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['Actors']))

    def test_get_all_movies(self):
        res = self.client().get('/movies',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])

    # def test_delete_actor(self):

    #     res=self.client().delete('/actors/1' , headers=self.producer_header)

    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)

    def test_422_delete_actor_failure(self):

        res = self.client().delete('/actors/99',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        # self.assertEqual(data['message'] ,'Not found')

    # # def test_delete_movie(self):
    # #     res=self.client().delete('/movies/3' , headers=self.producer_header)
    # #     data=json.loads(res.data)
    # #     self.assertEqual(res.status_code,200)
    # #     self.assertEqual(data['success'],True)

    def test_delete_movie_failure(self):

        res = self.client().delete('/actors/99',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_actor(self):
        response = self.client().post('/actors', json=self.new_actor,
                headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_add_actor(self):

        response = self.client().post('/actors', json={},
                headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_movie(self):
        new_movie = {'title': 'aihaga', 'release_date': '5-7-1998',
                     'actor_id': 1}
        response = self.client().post('/movies', json=new_movie,
                headers=self.producer_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failure_add_movie(self):
        response = self.client().post('/movies', json={},
                headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_edit_actorss(self):
        new_actorr = {'name': 'maaai'}
        response = self.client().patch('/actors/2', json=new_actorr,
                headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failure_edit_actorss(self):

        # Assume that patch fails when id is not found and we do not get a new body , mafish json asln myf34 23ml json={} keda de m3naha #3delha 5leha fadia

        response = self.client().patch('/actors/99',
                headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_edit_moviess(self):
        new_moviie = {'title': 'nasksdkda'}

        response = self.client().patch('/movies/3', json=new_moviie,
                headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failure_edit_moviess(self):

        # Assume that patch fails when id is not found and we do not get a new body , mafish json asln myf34 23ml json={} keda de m3naha #3delha 5leha fadia

        response = self.client().patch('/movies/99',
                headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable

if __name__ == '__main__':
    unittest.main()
