import unittest
from unittest.mock import patch, MagicMock
from main import TikTok
from utils import TimeoutError, HTTPError

class TestTikTok(unittest.TestCase):
    """
    Tests for the TikTok API client class.
    """

    def setUp(self):
        """Set up for test methods."""
        self.client_key = "test_key"
        self.client_secret = "test_secret"
        self.redirect_uri = "https://example.com/callback"
        self.tiktok = TikTok(self.client_key, self.client_secret, self.redirect_uri)

    def test_initialization(self):
        """Tests the initialization of the TikTok class."""
        self.assertEqual(self.tiktok.client_key, self.client_key)
        self.assertEqual(self.tiktok.client_secret, self.client_secret)
        self.assertEqual(self.tiktok.redirect_uri, self.redirect_uri)
        self.assertIsNotNone(self.tiktok.code_verifier)
        self.assertEqual(len(self.tiktok.code_verifier), 86) # Length of urlsafe token with 64 bytes
        self.assertEqual(self.tiktok.state, "")

        custom_scopes = ["video.list", "user.info.basic"]
        tiktok_custom_scopes = TikTok(self.client_key, self.client_secret, self.redirect_uri, scopes=custom_scopes)
        self.assertEqual(tiktok_custom_scopes.AUTH_SCOPE, custom_scopes)

    def test_generate_code_verifier(self):
        """Tests the generation of the code verifier."""
        verifier = self.tiktok._generate_code_verifier()
        self.assertIsInstance(verifier, str)
        self.assertEqual(len(verifier), 86)

    def test_generate_code_challenge(self):
        """Tests the generation of the code challenge."""
        verifier = "this_is_a_test_code_verifier_with_enough_length"
        challenge = self.tiktok._generate_code_challenge(verifier)
        self.assertIsInstance(challenge, str)
        self.assertNotEqual(challenge, True)