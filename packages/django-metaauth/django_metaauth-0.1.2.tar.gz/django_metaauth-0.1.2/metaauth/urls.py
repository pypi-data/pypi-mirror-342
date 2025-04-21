from django.urls import path, include
from .views import OauthInstallView, OauthRedirectView, success_view, error_view

urlpatterns = [
    path("install", view=OauthInstallView.as_view(), name="meta-install"),
    path("redirect", view=OauthRedirectView.as_view(), name="meta-redirect"),
    path("success", success_view, name="success"),  # Define the success URL
    path("error", error_view, name="error"),  # Define the success URL
]
