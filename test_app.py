import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        Cast_Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBGUGxaVWxPeHp2Ym5XLW14ekpURyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC1jYXBzdG9uZS1hbmp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTcwNzA5YTMzZjY5MjAwNzA0YmZiYjkiLCJhdWQiOiJjYXN0YWdlbmN5IiwiaWF0IjoxNjM1OTY2MjQ1LCJleHAiOjE2MzYwNTI2NDUsImF6cCI6InBmYklKeEQ0UkdJeXlLd1FXS1p3OXZmd0hqMkhBd2NTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ydnSkVQEF3IMq1vOJnJCcSoC-TmTESpySHWc0HJNyg7eDCaFz4_peh2-eUj4uAMp4F7a4nLQ3oPXBwC17JR2ZuYCJT6_anZiVXi418N6guIiv8RGgTvodxsFqWpMs-T76bf8UscMXk1KPoG5qF9_m9774h-LO9GrhhTnjdbYZI9fyeFfIKWXUcLUD-jLZnz33eI1RuBXYticBWGQyk2zPKRjfEvzSRj1qertAuCBBTwYLhDx2a5RWoKVOLUqJWf64kTbrDjKbNY4m9r0t95uPQAwwAi_xVOvxJyKtBfhmf_wPqT8l6nm4dkdB4oL-RWnTs_IzQfiBQ7QQA-skx1W4g'
        Cast_Director_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBGUGxaVWxPeHp2Ym5XLW14ekpURyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC1jYXBzdG9uZS1hbmp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTZmMzJhOWZmODZmNjAwNmEzYjM5MDYiLCJhdWQiOiJjYXN0YWdlbmN5IiwiaWF0IjoxNjM1OTY2NDU2LCJleHAiOjE2MzYwNTI4NTYsImF6cCI6InBmYklKeEQ0UkdJeXlLd1FXS1p3OXZmd0hqMkhBd2NTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.BV5OzrzuDiVaEN5TjKzLdUeWQ9yy7yaQXuAU_3dfTP2Hta61cuMdxptNqs7n1JJYw_GwrRzgOfY_48jYRHpidxAItKHh_JO3pnAXb20aprGfka7aOZRMIrODkHcGhXlOzl3uzBlvIQMHOn26LnIofBE1ajZWltFHynEjUzMmbnJDaJQCRLnXBY-cSSVlr2hdEHje1HTlzCbJUMj3GcvE8XMAB75Kh9doPg77Y4bFbJ6Pedlx9Ox3EFdH33ajpb-uYl9e94C3FtpSzowGZ8YrVWyFw-lF1zOg9wpOtgskECefQAh-Ik0YqkwZcaZc6ZqZnsgqDpZqa_WOJqFm2lQUHw'
        Exec_Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBGUGxaVWxPeHp2Ym5XLW14ekpURyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC1jYXBzdG9uZS1hbmp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTZmMzJjNDFlMzhkOTAwNjg2MTdhNmYiLCJhdWQiOiJjYXN0YWdlbmN5IiwiaWF0IjoxNjM1OTY2MzcwLCJleHAiOjE2MzYwNTI3NzAsImF6cCI6InBmYklKeEQ0UkdJeXlLd1FXS1p3OXZmd0hqMkhBd2NTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.T9T7mc09XklvKp4pjkbZvg52a84dF7pCO00LZgiIrnQtt1UFY9BzejXG-2pqPyVrld-OmO_S2y9Hye6ewIz7KiYkiNP9Pj9zpo1WMPKC483wj3BxHM48lSAlRSQwSXmMO1EYYh1TZ8_pw8cxQAKxGvKHZz3aQ0b59-tNh1o7ZAOrouAvvFr7k4LO7sPA_Znm-KsAsgLx-WXVlXISL4-JHRQuNhmgenG7umf3ZGEMmKv4x_CCWVK58_Yy9UKHOxbB4UnHpu8UKcvXaj3s259RRg8D-6tpnZW0I4NGARuQKY0ycTlBXbhpEtoOwxUghqbvQclePTcirtm2xPjIsyxf7A'



        self.cast_assist_auth_header = {'Authorization':
                                      'Bearer ' + Cast_Assistant_Token}
        self.cast_director_auth_header = {'Authorization':
                                     'Bearer ' + Cast_Director_Token}
        self.exec_producer_auth_header = {'Authorization':
                                     'Bearer ' + Exec_Producer_Token}
        


        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        '''
        Test data for actors and movies
        Roles: Casting Assistant, Casting Director, Executive producer
        '''

        self.new_actor1 = {
            'name': 'Jerry',
            'gender': 'Male',
            'age': 45
        }

        self.new_actor2 = {
            'name': 'George',
            'gender': 'Male',
            'age': 45
        }

        self.new_actor3 = {
            'name': 'Kramer',
            'age': 40
        }

        self.new_movie1={
            'title':'Dune',
            'release_date':'2020-10-22'}

        self.new_movie_missing={
            'title':'Warning',
            }

        self.new_movie2={
            'title':'Antlers',
            'release_date':'2020-10-22' #patch 2020-10-29
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests:
        One test for success behavior of each endpoint
        One test for error behavior of each endpoint
        At least two tests of RBAC for each role
    """
    #Test cases for Actors end points.
    #testing casting assistant RBAC along with get actors.
    def test_get_actors(self):
        res = self.client().get('/actors?page=1', 
                                    headers=self.cast_assist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)
    
    #testing positive RBAC with casting director
    def test_rbac_get_actors(self):
        res = self.client().get('/actors?page=1', 
                                    headers=self.cast_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)
    
    #testing post for actors
    def test_post_actor(self):
        res = self.client().post('/actors', 
                                        json=self.new_actor1,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        actor = Actors.query.filter_by(id=data['actor_added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(actor)
    
    def test_post_actor1(self):
        res = self.client().post('/actors', 
                                        json=self.new_actor2,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        actor = Actors.query.filter_by(id=data['actor_added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(actor)

    #testing negative case for post actor
    def test_post_actor_422_missing_gender(self):
        res = self.client().post('/actors', 
                                        json=self.new_actor3,
                                        headers=self.cast_director_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #Patch positive testing
    def test_patch_actor(self):
        update_actor = {'age':50}
        res = self.client().patch('/actors/1', 
                                        json=update_actor,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor-updated'],1)
    
    #Patch negative testing
    def test_patch_404_actor_not_found(self):
        update_actor = {'age':50}
        res = self.client().patch('/actors/11', 
                                        json=update_actor,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    #delete positive test case
    def test_delete_actor(self):
        new_actor = {
            'name': 'Niles',
            'gender': 'Male',
            'age': 50
        }
        res = self.client().post('/actors', 
                                        json=new_actor,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        delete_actor = data['actor_added']
        res = self.client().delete('/actors/{}'.format(delete_actor), 
                                        headers=self.exec_producer_auth_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted-actor'],delete_actor)
    
    #delete negative case
    def test_delete_actor_404_not_found(self):
        res = self.client().delete('/actors/99', 
                                        headers=self.cast_director_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    #Movies test cases
    def test_get_movies(self):
        res = self.client().get('/movies?page=1', headers=self.exec_producer_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    #testing post for movies
    def test_post_movie(self):
        res = self.client().post('/movies', 
                                        json=self.new_movie1,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        movie = Movies.query.filter_by(id=data['new-movie-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(movie)

    def test_post_movie2(self):
        res = self.client().post('/movies', 
                                        json=self.new_movie2,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        movie = Movies.query.filter_by(id=data['new-movie-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(movie)
    
    

    #testing negative case for post movie
    def test_post_movie_422_missing_release_date(self):
        res = self.client().post('/movies', 
                                        json=self.new_movie_missing,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #Patch movie positive testing
    def test_patch_movie(self):
        update_movie = {
            'title': 'Apex',
            'release_date':'2020-10-29'}
        res = self.client().patch('/movies/1', 
                                        json=update_movie,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie-updated'],1)
    
    #Patch movie negative testing
    def test_patch_404_movie_not_found(self):
        update_movie = {'release_date':'2020-10-29'}
        res = self.client().patch('/actors/11', 
                                        json=update_movie,
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    #delete movie positive test case
    def test_delete_movie(self):
        
        res = self.client().delete('/movies/2', 
                                        headers=self.exec_producer_auth_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted-movie'],2)
    
    #delete movie negative case
    def test_delete_movie_404_not_found(self):
        res = self.client().delete('/movies/99', 
                                        headers=self.exec_producer_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')
    
    #testing RBAC - without authorization -  should result negative
    def test_without_auth(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    #testing RBAC - testing casting director deleting a movie should result negative
    def test_wrong_auth(self):
        res = self.client().delete('/movies/1', 
                                        headers=self.cast_director_auth_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
