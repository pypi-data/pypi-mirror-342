from django.urls import path
from .views import (
    InstallView,
    RedirectView,
)

app_name = "googleadsauth"

urlpatterns = [
    path("oauth/install", view=InstallView.as_view(), name="oauth-install"),
    path("oauth/redirect", view=RedirectView.as_view(), name="oauth-redirect"),
]
