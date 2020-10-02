import unittest
from src.authorisation import *
from src.main import *

client = PkceAuthCode()


class TestStatusCodes(unittest.TestCase):
    def test_uri(self):
        result = client.get_auth_uri()
        self.assertIsInstance(result, str)

    def test_auth_uri(self):
        result = PkceAuthCode().get_auth_uri()
        self.assertIsInstance(result, str)

