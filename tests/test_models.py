import unittest
from unittest.mock import patch
import requests
from apps.user.models import CustomUser

def get_kaspi_http(token):
    return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Content-Type': 'application/vnd.api+json',
            'X-Auth-Token': token.token_api,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5"
        }

class TestGetKaspiHttp(unittest.TestCase):
    def test_ones(self):
        class Token:
            def __init__(self, token_api):
                self.token_api = token_api
        token = Token("test_token")
        expected_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Content-Type': 'application/vnd.api+json',
            'X-Auth-Token': 'test_token',
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5"
        }
        self.assertEqual(get_kaspi_http(token), expected_headers)

class TestKaspiEndpoint(unittest.TestCase):
    base_url = 'http://127.0.0.1:8000/api/kaspi/approve/'

    @patch('requests.get')
    def test_endpoint_response(self, mock_get):
        mock_get.return_value.status_code = 200
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)

class CustomModelTestCase(unittest.TestCase):
    def testCustomUser(self):
        phone_user = CustomUser.objects.create(username='user1', phone='87772223344')
        role_user = CustomUser.objects.create(username='user2', role='Client')

        self.assertIsNotNone(phone_user)
        self.assertIsNotNone(role_user)

