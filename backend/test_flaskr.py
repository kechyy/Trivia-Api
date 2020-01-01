import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'psql', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'New question',
            'answer': 'New answer',
            'category': 3,
            'difficulty': 2
        }

        self.quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Art',
                'id': 1,
            }
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
    This test validates all successful operations and expected errors.
    
    """


    def test_get_categories(self):
        """
        This test assert true for all available categories and assert false if if category available 
    
        """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        if data['total_categories'] == 0:
            self.assertFalse(data['categories'])
            self.assertFalse(data['total_categories'])
        else:
            self.assertTrue(data['categories'])
            self.assertTrue(data['total_categories'])

    def test_get_false_route(self):
        """
        This test assert that status code 404 is returned if route is not found
    
        """
        res = self.client().get('/youuu')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        """
        This test returns questions and categories if assertion returns true returns false if total questions returns false.
    
        """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        if data['total_questions'] == 0:
            self.assertFalse(data['questions'])
            self.assertFalse(data['total_questions'])
        else:
            self.assertTrue(data['categories'])
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])

    def test_get_questions_beyond_limit(self):
         """
        This test returns success when page is found but return false when page is not found.
    
        """
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_question(self):
         """
        This test returns success if a specific question is found
        """
        res = self.client().get('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_question_not_found(self):
         """
        This test returns false when no specific question is found
        """
        res = self.client().get('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    

    def test_get_category_not_found(self):
         """
        This test returns 404 when no specific category is found
    
        """
        res = self.client().get('/categories/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_get_category_questions(self):
         """
        This test returns true when a questions are found under a specific category.
    
        """
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_questions'], 4)

    def test_get_category_questions_not_found(self):
        """
        This test returns false when question is found under a specific category.
    
        """
        res = self.client().get('/categories/99987699/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_create_new_question(self):
        """
        This test validates that new question is created with status code of 201
        """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_question_incorrect(self):
        """
        This test return message with 422 status code for unprocessable request for questions.
    
        """
        res = self.client().post('/questions', json={'question': 'Test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertTrue(data['message'])

    def test_search_for_questions(self):
        """
        This test return 200 status code for successful question title found
    
        """
        res = self.client().post('/questions', json={'search': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)

    def test_search_for_questions_no_results(self):
        """
        This test return 200 status code for question search not found
    
        """
        res = self.client().post('/questions', json={'search': 'zombie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_delete_question(self):
        """
        This test return 200 status code for a successful delete question
    
        """
        last = Question.query.order_by(Question.id.desc()).first()
        res = self.client().delete(f'/questions/{last.id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == last.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_not_found(self):
        """
        This test return 404 status code for an invalid delete route
    
        """
        res = self.client().delete(f'/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_post_quizzes(self):
        """
         This test return all quizzes if assertion returns true with 200 status code.
    
        """
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['answer'])
        self.assertTrue(data['question']['difficulty'])
        self.assertTrue(data['question']['category'])

    def test_post_quizzes_incorrect(self):
        """
        This test return message with 422 status code for unprocessable request for quizzes.
    
        """
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertTrue(data['message'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


# API Documentation Link
# URL
# https://documenter.getpostman.com/view/6380213/SW7c3Ten