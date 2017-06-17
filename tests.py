""" Defines tests """
import unittest
import json
import app


class AppTestCase(unittest.TestCase):
    """ Defines app and api test examples """

    def setUp(self):
        """ Sets up env for tests """
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        """ Tears down after tests """
        pass

    def test_index(self):
        """ Tests GET / """
        response = self.app.get('/')
        assert response.status == "200 OK"
        assert "Web API".encode('utf-8') in response.data

    def test_api_candidates(self):
        """ Tests GET /api/candidates """
        response = self.app.get('/api/candidates')
        tmp_data = json.loads(response.data)
        assert len(tmp_data['candidates']) == 3


if __name__ == '__main__':
    unittest.main()
