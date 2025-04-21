import uuid
import os
from django.views.generic.base import RedirectView
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from .models import Token  # Import the Token model
import logging
import requests
from metaauth import settings as app_settings

logger = logging.getLogger(__name__)

from django.shortcuts import render


def success_view(request):
    return render(request, "metaauth/success.html")


def error_view(request):
    return render(request, "metaauth/error.html")


class OauthInstallView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        client_id = app_settings.get_facebook_app_id()
        state = str(uuid.uuid4())
        self.request.session["state"] = state
        redirect_uri = app_settings.get_facebook_redirect_uri()
        config_id = app_settings.get_facebook_config_id()
        params = {
            "client_id": client_id,
            "response_type": "code",
            "scope": app_settings.get_facebook_required_scopes(),
            "state": state,
            "redirect_uri": redirect_uri,
            "config_id": config_id
        }

        oauth_url = self._construct_url(
            f"https://www.facebook.com/{app_settings.get_facebook_api_version()}/dialog/oauth",
            params,
        )
        return oauth_url

    def _construct_url(self, base_url, params):
        """Helper method to construct a URL with query parameters."""
        return f"{base_url}?{urlencode(params, doseq=True)}"


class OauthRedirectView(View):

    def get(self, request, *args, **kwargs):
        if "code" not in request.GET or "state" not in request.GET:
            logger.error("Missing 'code' or 'state' in callback parameters")
            return HttpResponseRedirect(
                app_settings.get_error_url()
            )  # Redirect to an error page

        code = request.GET["code"]
        token_url = f"https://graph.facebook.com/{app_settings.get_facebook_api_version()}/oauth/access_token"
        params = {
            "client_id": app_settings.get_facebook_app_id(),
            "client_secret": app_settings.get_facebook_app_secret(),
            "code": code,
            "redirect_uri": app_settings.get_facebook_redirect_uri(),
        }

        try:
            logger.debug("Exchanging code %s for access token", code)
            response = requests.get(token_url, params=params)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            token_data = response.json()
            logger.info(token_data)
        except requests.exceptions.RequestException as e:
            logger.error("Failed to get access token: %s", e)
            return HttpResponseRedirect(
                app_settings.get_error_url()
            )  # Redirect to an error page

        if "access_token" not in token_data:
            logger.error("Access token not found in the response")
            return HttpResponseRedirect(
                app_settings.get_error_url()
            )  # Redirect to an error page

        access_token = token_data["access_token"]
        expires_in = token_data.get(
            "expires_in"
        )  # Get the expires_in value, or None if not present
        token_obj = Token.objects.create(token=access_token, expires_in=expires_in)
        logger.info("Token saved successfully")

        return HttpResponseRedirect(app_settings.get_success_url())
