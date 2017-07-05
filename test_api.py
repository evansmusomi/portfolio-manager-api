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
        tmp_data = json.loads(response.data)
        assert tmp_data['candidates']

    def test_api_candidate_by_id_OK(self):
        """ Tests GET /api/candidates/<string:candidate_id>"""
        response = self.app.get('/api/candidates/1',
                                headers={"MY_AUTH_TOKEN": Config.AUTH_TOKEN})
        tmp_data = json.loads(response.data)
        assert len(tmp_data['candidate']) == 1
