from django.urls import path, include

urlpatterns = [
    path("meta/oauth/", include("metaauth.urls")),
]
