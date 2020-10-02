import unittest
from authorisation import PkceAuthCode


class TestStatusCodes(unittest.TestCase):
    def test_auth_uri(self):
        result = PkceAuthCode().get_auth_uri()
        self.assertIsInstance(result, str)

    def test_auth_token(self):
        result = PkceAuthCode().get_access_token()
        self.assertTrue(result, True)

    def test_token_refresh(self):
        pass

    def test_search(self):
        pass

    def test_playlist(self):
        pass

