from django.test import TestCase
from metaauth.models import Token
from django.utils import timezone


class TokenModelTest(TestCase):
    def test_token_creation(self):
        token = Token.objects.create(
            token="test_token_string", expires_in=3600, external_id="test_external_id"
        )

        self.assertEqual(token.token, "test_token_string")
        self.assertEqual(token.expires_in, 3600)
        self.assertEqual(token.external_id, "test_external_id")

        # Check that created_at is populated
        self.assertIsNotNone(token.created_at)
        self.assertTrue(token.created_at <= timezone.now())

    def test_token_string_representation(self):
        token = Token.objects.create(token="test_token_string")
        self.assertEqual(str(token), "test_token_string")
