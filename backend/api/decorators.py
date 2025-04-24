import logging
from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
# from orm.models import User, UserCompany
from orm.models import User
from _applibs.response import echo, Messages
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

logger = logging.getLogger(__name__)

def token_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Try to get the access token from cookies
        access_token = request.COOKIES.get('access')
        # logger.info(f"cookie access token: {access_token}")
        if not access_token:
            # Try to get the access token from the Authorization header
            auth_header = request.headers.get('Authorization')
            # logger.info(f"auth header: {auth_header}")
            if auth_header and auth_header.startswith('Bearer '):
                access_token = auth_header[len('Bearer '):]

        # logger.info(f"access token: {access_token}")

        if not access_token:
            return echo(status=status.HTTP_401_UNAUTHORIZED, msg="No access token found.")

        try:
            # Attempt to validate the access token
            payload = AccessToken(access_token).payload

           
        except InvalidToken:
            # Check for a refresh token if access token is invalid
            refresh_token = request.COOKIES.get('refresh')
            if not refresh_token:
                return echo(status=status.HTTP_401_UNAUTHORIZED, msg="Invalid access token and no refresh token provided.")

            try:
                # Check if the refresh token is blacklisted
                if RefreshToken.is_blacklisted(refresh_token):
                    return echo(status=status.HTTP_401_UNAUTHORIZED, msg="Refresh token is blacklisted.")
                
                # Validate the refresh token and issue a new access token
                refresh = RefreshToken(refresh_token)
                new_access_token = refresh.access_token

                # Optionally: Save the new access token to the user's cookies
                response = JsonResponse({"message": "Token refreshed"})
                response.set_cookie('access', str(new_access_token), httponly=True, secure=True, samesite='None')

                # Set the new access token in the request
                payload = new_access_token.payload

            except (TokenError, InvalidToken) as e:
                return echo(status=status.HTTP_401_UNAUTHORIZED, msg=f"Refresh token is invalid: {str(e)}")

        except TokenError as e:
            return echo(status=status.HTTP_401_UNAUTHORIZED, msg=f"Token error: {str(e)}")

        # Validate the user
        user = User.objects.filter(id=payload['user_id']).first()
        if not user:
            return echo(status=status.HTTP_401_UNAUTHORIZED, msg='User not found!')

        request.user = user

        # Call the original view
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view

