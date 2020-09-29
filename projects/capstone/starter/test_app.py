import os ,unittest ,json
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, String, Integer, create_engine ,DateTime 
from app import create_app
from models import setup_db, Actor ,Movie


class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):

        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgresql://postgres:1234@localhost:5432/castingagency"
        setup_db(self.app)
        # binds the app to the current context
        with self.app.app_context():

            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #give the attribuites of the class any values
        # self.new_actor={ 
        #     'id' :1,
        #     'name':'Adel Emam' ,
        #     'age' :50,
        #     'gender' : 'Male' }
        # self.new_movie={ 
        #     'id' :2,
        #     'title':'aihaga' ,
        #     'release_date' : "5-7-1998"
        #     }
    
          
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_actors(self):

    
        res=self.client().get('/actors')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['Actors']))


    def test_get_all_movies(self):
        res=self.client().get('/movies')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['Movies'])


    # def delete_actor(self):
    #     res=self.client().get('/actors/1')
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['id'],1)

    # def delete_actor_failure(self):
    #     res=self.client().get('/actors/99999')
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,422)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'] ,'unprocessable')
   
    
    
    # def delete_movie(self):
    #     res=self.client().get('/actors/2')
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['id'],2)

    # def delete_movie_failure(self):

    #     res=self.client().get('/actors/99999')
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,422)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'] ,'unprocessable')

    # def post_actor(self):

    #     actor_before_add = len(Actor.query.all())
    #     response = self.client().post('/actors' , json=self.new_actor)
    #     data=json.loads(response.data)
    #     actor_after_add=len(Actor.query.all())
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertTrue(actor_before_add - actor_after_add == 1)

    # def test_failure_add_actor(self):
  
    #     response = self.client().post('/actors' , json={})
    #     data=json.loads(response.data)
    #     self.assertEqual(response.status_code,422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'] ,'unprocessable')

    # def post_movie(self):
    #     movie_before_add = len(Movie.query.all())
    #     response = self.client().post('/movies' , json=self.new_movie)
    #     data=json.loads(response.data)
    #     movie_after_add=len(Movie.query.all())
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertTrue(movie_before_add - movie_after_add == 1)

    # def test_failure_add_movie(self):
    #     response = self.client().post('/movies' , json={})
    #     data=json.loads(response.data)
    #     self.assertEqual(response.status_code,422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'] ,'unprocessable')

    # def edit_actorss(self):
    #     new_actor={
    #         "name":"Arwaaaaaaaaaa"
    #         }
    #     response = self.client().post('/actors/1' , json=self.new_actor)

    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)

    # def failure_edit_actorss(self):
    #     #Assume that patch fails when id is not found and we do not get a new body , mafish json asln myf34 23ml json={} keda de m3naha #3delha 5leha fadia
    #     response = self.client().post('/actors/99999' )
    #     self.assertEqual(response.status_code,404)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'] ,'Resource is not found')

    # def edit_moviess(self):
    #     new_movie={
    #         "title":"CloudyFilm"
    #         }
    #     response = self.client().post('/movies/2' , json=self.new_movie)

    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)

    # def failure_edit_moviess(self):
    #     #Assume that patch fails when id is not found and we do not get a new body , mafish json asln myf34 23ml json={} keda de m3naha #3delha 5leha fadia
    #     response = self.client().post('/movies/99999' )
    #     self.assertEqual(response.status_code,404)
    #     self.assertEqual(data['success'],False)



   
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()