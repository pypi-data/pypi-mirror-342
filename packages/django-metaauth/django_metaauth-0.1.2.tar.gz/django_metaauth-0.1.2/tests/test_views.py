from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
from metaauth.views import OauthInstallView, OauthRedirectView
from metaauth.models import Token
import json


class OauthInstallViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_redirect_url(self):
        request = self.factory.get("/meta/oauth/install")
        request.session = {}

        view = OauthInstallView()
        view.request = request

        url = view.get_redirect_url()

        self.assertIn("client_id=test-app-id", url)
        self.assertIn("response_type=code", url)
        self.assertIn("redirect_uri=http", url)
        self.assertTrue("state" in request.session)


class OauthRedirectViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("metaauth.views.requests.get")
    def test_successful_token_exchange(self, mock_get):
        # Mock the response from the API
        mock_response = type(
            "MockResponse",
            (),
            {
                "json": lambda self: {"access_token": "test_token", "expires_in": 3600},
                "raise_for_status": lambda self: None,
            },
        )()
        mock_get.return_value = mock_response

        # Create the request
        request = self.factory.get(
            "/meta/oauth/redirect?code=test_code&state=test_state"
        )
        request.session = {"state": "test_state"}

        # Call the view
        view = OauthRedirectView()
        response = view.get(request)

        # Check that a token was created
        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.first()
        self.assertEqual(token.token, "test_token")
        self.assertEqual(token.expires_in, 3600)
