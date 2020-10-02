import unittest
from authorisation import *
from main import *


class TestStatusCodes(unittest.TestCase):
    def test_uri(self):
        result = client.get_auth_uri()
        self.assertIsInstance(result, str)

    def test_auth_uri(self):
        result = PkceAuthCode().get_auth_uri()
        self.assertIsInstance(result, str)

