from fastapi.testclient import TestClient

import unittest
from src.api import app
import httpx


class TestAPI(unittest.TestCase):

    client = TestClient(app)

    def test_healthz_get(self):
        """
        Test the health check endpoint.
        """
        response = self.client.get("http://localhost:8000/healthz")
        self.assertEqual(response.status_code, 200)

    def test_healthz_post(self):
        """
        Test the health check endpoint with a POST request.
        """
        response = self.client.post("http://localhost:8000/healthz")
        self.assertEqual(response.status_code, 405)

    def test_healthz_put(self):
        """
        Test the health check endpoint with a PUT request.
        """
        response = self.client.put("http://localhost:8000/healthz")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
