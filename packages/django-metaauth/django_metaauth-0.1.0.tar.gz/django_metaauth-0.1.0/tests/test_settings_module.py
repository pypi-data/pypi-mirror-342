from django.test import TestCase, override_settings
from metaauth import settings as app_settings


class SettingsTest(TestCase):
    def test_default_settings(self):
        """Test that default settings are available when not overridden."""
        self.assertEqual(app_settings.get_facebook_api_version(), "v21.0")
        self.assertEqual(
            app_settings.get_facebook_required_scopes(),
            ["ads_management", "pages_show_list"],
        )
        self.assertEqual(app_settings.get_success_url(), "/meta/oauth/success")
        self.assertEqual(app_settings.get_error_url(), "/meta/oauth/error")

    @override_settings(METAAUTH_FACEBOOK_API_VERSION="v22.0")
    def test_custom_api_version(self):
        """Test that settings can be overridden by project settings."""
        self.assertEqual(app_settings.get_facebook_api_version(), "v22.0")

    @override_settings(METAAUTH_SUCCESS_URL="/custom/success/url")
    def test_custom_success_url(self):
        """Test that URL settings can be overridden."""
        self.assertEqual(app_settings.get_success_url(), "/custom/success/url")
