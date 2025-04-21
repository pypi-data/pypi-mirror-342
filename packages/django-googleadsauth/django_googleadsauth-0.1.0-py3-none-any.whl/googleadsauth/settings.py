from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os


class GoogleAdsSettings:
    """
    Settings class for Google Ads integration
    Handles configuration from Django settings and provides default values where appropriate
    """

    @property
    def CLIENT_SECRET_PATH(self):
        """Path to Google Ads API client secret JSON file"""
        return getattr(settings, "GOOGLE_ADS", {}).get("CLIENT_SECRET_PATH", None)

    @property
    def REDIRECT_URI(self):
        """URI to redirect to after Google OAuth authentication"""
        return getattr(settings, "GOOGLE_ADS", {}).get("REDIRECT_URI", None)

    @property
    def DEVELOPER_TOKEN(self):
        """Google Ads API developer token"""
        return getattr(settings, "GOOGLE_ADS", {}).get("DEVELOPER_TOKEN", None)

    @property
    def CLIENT_ID(self):
        """Google Ads API client ID"""
        return getattr(settings, "GOOGLE_ADS", {}).get("CLIENT_ID", None)

    @property
    def CLIENT_SECRET(self):
        """Google Ads API client secret"""
        return getattr(settings, "GOOGLE_ADS", {}).get("CLIENT_SECRET", None)

    @property
    def TOKEN_URI(self):
        """Google OAuth token URI"""
        return getattr(settings, "GOOGLE_ADS", {}).get(
            "TOKEN_URI", "https://oauth2.googleapis.com/token"
        )

    @property
    def MANAGER_ACCOUNT_ID(self):
        """Optional Google Ads manager account ID"""
        return getattr(settings, "GOOGLE_ADS", {}).get("MANAGER_ACCOUNT_ID", None)

    def validate_settings(self):
        """
        Validate that all required settings are provided
        Raises ImproperlyConfigured if any required settings are missing
        """
        required_settings = [
            "CLIENT_SECRET_PATH",
            "REDIRECT_URI",
            "DEVELOPER_TOKEN",
            "CLIENT_ID",
            "CLIENT_SECRET",
        ]

        missing_settings = []
        for setting in required_settings:
            if not getattr(self, setting):
                missing_settings.append(setting)

        if missing_settings:
            raise ImproperlyConfigured(
                f"Google Ads API settings are missing: {', '.join(missing_settings)}. "
                f"Please provide these in your Django settings under the GOOGLE_ADS dictionary."
            )

        # Validate that the client secret file exists
        if not os.path.exists(self.CLIENT_SECRET_PATH):
            raise ImproperlyConfigured(
                f"Google Ads API client secret file not found at {self.CLIENT_SECRET_PATH}."
            )


# Create a global instance of the settings
googleads_settings = GoogleAdsSettings()
