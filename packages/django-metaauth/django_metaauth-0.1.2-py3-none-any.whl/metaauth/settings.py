from django.conf import settings


def get_setting(name, default):
    """
    Helper function to get settings with a defined fallback.
    This also makes it easier to test settings overrides.
    """
    return getattr(settings, name, default)


# Meta API settings
def get_facebook_app_id():
    return get_setting("METAAUTH_FACEBOOK_APP_ID", None)


def get_facebook_app_secret():
    return get_setting("METAAUTH_FACEBOOK_APP_SECRET", None)


def get_facebook_redirect_uri():
    return get_setting("METAAUTH_FACEBOOK_REDIRECT_URI", None)


def get_facebook_api_version():
    return get_setting("METAAUTH_FACEBOOK_API_VERSION", "v22.0")


def get_facebook_required_scopes():
    return get_setting(
        "METAAUTH_FACEBOOK_REQUIRED_SCOPES", ["ads_management", "ads_read", "pages_show_list", "pages_manage_ads"]
    )


def get_facebook_config_id():
    return get_setting("METAAUTH_FACEBOOK_CONFIG_ID", None)


# URL settings
def get_success_url():
    return get_setting("METAAUTH_SUCCESS_URL", "/meta/oauth/success")


def get_error_url():
    return get_setting("METAAUTH_ERROR_URL", "/meta/oauth/error")


