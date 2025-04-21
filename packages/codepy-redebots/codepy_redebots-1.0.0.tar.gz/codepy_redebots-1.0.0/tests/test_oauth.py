import unittest
from codepy import OAuth

class TestOAuth(unittest.TestCase):
    def test_iniciar_oauth(self):
        oauth = OAuth(client_id="123", client_secret="secret", redirect_uri="http://example.com")
        self.assertEqual(oauth.client_id, "123")

if __name__ == "__main__":
    unittest.main()