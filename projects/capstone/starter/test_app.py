import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine ,DateTime ,Date,db ,create_app
from models import setup_db, Actor ,Movie

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):

        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://postgres:123@localhost:5432/castingagency"
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():

            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #give the attribuites of the class any values
        self.new_actor={ 
            'name':'Adel Emam' ,
            'age' :50,
            'gender' : 'Male' }

          
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def get_all_actors(self):
    
        res=self.client().get('/actors')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['Actors'])
    def get_all_movies(self):

    
        res=self.client().get('/movies')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])


    def delete_actor(self):
        res=self.client().get('/actors/1')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def delete_actor_failure(self):
        res=self.client().get('/actors/99999')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['id'])

        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()