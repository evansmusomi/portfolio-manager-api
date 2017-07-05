""" Defines tests """
import unittest
import json
import app
from settings import Config


class ApiTestCase(unittest.TestCase):
    """ Defines API test examples """

    def setUp(self):
        """ Sets up env for tests """
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_api_candidates_OK(self):
        """ Tests GET /api/candidates """
        response = self.app.get('/api/candidates')
        temp_data = json.loads(response.data)
        assert temp_data['candidates'] is not None

    def test_api_candidate_by_id_OK(self):
        """ Tests GET /api/candidates/<string:candidate_id>"""
        response = self.app.get('/api/candidates/1',
                                headers={"MY_AUTH_TOKEN": Config.AUTH_TOKEN})
        temp_data = json.loads(response.data)
        candidate = temp_data["candidate"][0]

        assert candidate is not None
        assert candidate["first_name"] == "John"
        assert candidate["id"] == 1

    def test_api_candidate_by_id_FAIL(self):
        """ Tests GET /api/candidates/<string:candidate_id> with invalid TOKEN """
        response = self.app.get('/api/candidates/1',
                                headers={"MY_AUTH_TOKEN": "INVALID"})

        assert response.status_code == 401
        assert response.headers["X-APP-ERROR-CODE"] == "9500"
        assert response.headers["X-APP-ERROR-MESSAGE"] == "No valid authentication token found in request"
