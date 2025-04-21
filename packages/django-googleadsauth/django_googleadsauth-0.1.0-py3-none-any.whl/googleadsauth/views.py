import logging
import os
import hashlib
import json
from urllib.parse import urlencode

from django.shortcuts import redirect, render
from django.conf import settings
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from google_auth_oauthlib.flow import Flow
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import Token, CampaignStatus
from .settings import googleads_settings

logger = logging.getLogger(__name__)






class InstallView(APIView):
    """
    View for initiating the Google OAuth flow.
    This redirects the user to the Google OAuth consent screen.
    """

    permission_classes = []  # No permission required for the install view

    def get(self, request, *args, **kwargs):
        # Get settings from the settings module
        client_secrets_path = googleads_settings.CLIENT_SECRET_PATH
        redirect_uri = googleads_settings.REDIRECT_URI
        scopes = ["https://www.googleapis.com/auth/adwords"]

        try:
            flow = Flow.from_client_secrets_file(client_secrets_path, scopes=scopes)
            flow.redirect_uri = redirect_uri

            # Generate a state token to prevent CSRF
            passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()
            request.session["passthrough_val"] = passthrough_val

            authorization_url, state = flow.authorization_url(
                access_type="offline",
                state=passthrough_val,
                prompt="consent",
                include_granted_scopes="true",
            )

            # If this is an API call and not a browser redirect, return the URL
            if request.headers.get("Accept") == "application/json":
                return Response(authorization_url)

            return redirect(authorization_url)

        except Exception as e:
            logger.error(f"Error in OAuth install process: {str(e)}")
            return Response(
                {"error": f"Error in OAuth install process: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RedirectView(APIView):
    """
    View for handling the OAuth redirect from Google.
    This processes the authorization code and saves the token.
    """

    permission_classes = []  # No permission required for the redirect view

    def get(self, request, *args, **kw):
        try:
            # Get settings from the settings module
            client_secrets_path = googleads_settings.CLIENT_SECRET_PATH
            redirect_uri = googleads_settings.REDIRECT_URI
            scopes = ["https://www.googleapis.com/auth/adwords"]

            # Verify state token to prevent CSRF
            passthrough_val = request.session.get("passthrough_val")
            state = request.GET.get("state")

            if passthrough_val != state:
                return Response(
                    {"error": "Invalid state parameter"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get the authorization code from the request
            code = request.GET.get("code")
            if not code:
                return Response(
                    {"error": "Authorization code not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Exchange authorization code for tokens
            flow = Flow.from_client_secrets_file(client_secrets_path, scopes=scopes)
            flow.redirect_uri = redirect_uri
            flow.fetch_token(code=code)

            # Get the refresh token
            refresh_token = flow.credentials.refresh_token
            if not refresh_token:
                return Response(
                    {"error": "No refresh token received"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Save the token to the database
            token = Token(token=refresh_token)
            token.save()

            # Return a success response
            return Response({"message": "Token saved successfully"})

        except Exception as e:
            logger.error(f"Error in OAuth redirect process: {str(e)}")
            return Response(
                {"error": f"Error in OAuth redirect process: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
