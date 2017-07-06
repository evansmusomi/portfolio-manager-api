""" Defines tests """
import unittest
import json
import app
from settings import Config


class ApiTestRoutes(unittest.TestCase):
    """ Defines API route test examples """

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


class ApiTestOperations(unittest.TestCase):
    """ Defines API (CRUD) oprerations test examples """

    def setUp(self):
        """ Sets up env for tests """

        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_api_candidate_create(self):
        """ Tests POST /api/candidates/ """

        candidate_data = dict(
            first_name="First",
            last_name="Last",
            email="last@first.com",
            phone="123-567-123",
            birthday="1989-01-21"
        )

        temp_data = self.api_candidate_create(candidate_data)

        assert temp_data["id"] is not None
        assert temp_data["url"] is not None
        self.api_test_candidate_read(temp_data["id"])

    def api_candidate_create(self, candidate_data):
        """ Returns created candidate with data provided """

        response = self.app.post('/api/candidates', data=candidate_data)
        return json.loads(response.data)

    def api_test_candidate_read(self, candidate_id):
        """ Tests Candidate Read operation works """

        response = self.app.get(
            '/api/candidates/' + str(candidate_id), headers={"MY_AUTH_TOKEN": Config.AUTH_TOKEN})

        temp_candidate = json.loads(response.data)
        candidate = temp_candidate["candidate"][0]

        assert candidate is not None
        assert candidate["first_name"] == "First"
        assert candidate["last_name"] == "Last"
        assert candidate["email"] == "last@first.com"

    def test_api_candidate_delete(self):
        """ Tests DELETE /api/candidate/<string:candidate_id> """

        candidate_data = dict(
            first_name="First",
            last_name="Last",
            email="last@first.com",
            phone="123-567-123",
            birthday="1989-01-21"
        )

        temp_data = self.api_candidate_create(candidate_data)

        response = self.app.delete("/api/candidate/" + str(temp_data["id"]))
        assert response.status_code == 200
