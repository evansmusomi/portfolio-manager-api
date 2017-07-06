""" Defines tests """
import unittest
import json
import app


class AppTestCase(unittest.TestCase):
    """ Defines app test examples """

    def setUp(self):
        """ Sets up env for tests """
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        """ Tears down after tests """
        pass

    def test_index_OK(self):
        """ Tests GET / """
        response = self.app.get('/')
        assert response.status == "200 OK"
        assert "Web API".encode('utf-8') in response.data

    def test_about_OK(self):
        """ Tests GET /about """
        response = self.app.get('/about')
        assert response.status == "200 OK"
        assert "About".encode('utf-8') in response.data

    def test_candidates_OK(self):
        """ Tests GET /candidates """
        response = self.app.get('/candidates')
        assert response.status == "200 OK"
        assert "Candidates".encode('utf-8') in response.data

    def test_crash_OK(self):
        """ Tests GET /crash """
        response = self.app.get('/crash')
        assert response.status == "200 OK"
        assert "Server crashed".encode('utf-8') in response.data
        assert "Try going Home".encode('utf-8') in response.data
