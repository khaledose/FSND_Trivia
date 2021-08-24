import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '123456789')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self. DB_PASSWORD, self.DB_HOST, self.DB_NAME)

        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    '''
    Tests retrieving paginated questions successfully
    '''
    def test_get_paginated_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) <= 10)

    '''
    Tests getting a question by ID successfully
    '''
    def test_get_question_success(self):
        res = self.client().get('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['question'],  None)

    '''
    Tests getting a question by ID that doesn't exist in the database
    '''
    def test_get_question_not_found(self):
        res = self.client().get('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests adding new question successfully
    '''
    def test_post_question_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        number_of_questions = data['total_questions']
        res = self.client().post('/questions', json={
            "answer": "Yellow", 
            "category": 1, 
            "difficulty": 1, 
            "question": "What is the color of a banana?"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'] == number_of_questions + 1)

    '''
    Tests searching for questions based on a search term successfully
    '''
    def test_search_question_success(self):
        res = self.client().post('/questions', json={'searchTerm': 'africa'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])

    '''
    Tests adding new question with Null json body
    '''
    def test_search_question_method_not_allowed(self):
        res = self.client().post('/questions', json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    '''
    Tests deleting a question by ID successfully
    '''
    def test_delete_question_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        number_of_questions = data['total_questions']
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question_id'], '5')
        self.assertTrue(data['total_questions'] == number_of_questions - 1)

    '''
    Tests deleting a question by ID that doesn't exist in the database
    '''
    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests getting questions related to a category successfully
    '''
    def test_get_questions_by_category_success(self):
        res = self.client().get('categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category']['id'], 2)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    '''
    Tests getting questions related to a category that doesn't exist
    '''
    def test_get_questions_by_category_not_found(self):
        res = self.client().get('categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()