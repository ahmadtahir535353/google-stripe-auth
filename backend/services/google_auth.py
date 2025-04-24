import logging
from typing import Optional
from django.conf import settings
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from orm.models import User
from _applibs.response import echo, Messages

def verify_google_token(id_token_str):
    try:
        logging.debug("Verifying Google ID token.")
        # Verify the token
        id_info = id_token.verify_oauth2_token(
            id_token_str, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        logging.info("Token verified successfully.")
        return id_info
    except ValueError as e:
        # Invalid token
        logging.error("Token verification failed: %s", str(e))
        return None

def google_auth_view(id_token_str):
    if not id_token_str:
        logging.warning("ID token is missing in request.")
        return echo(status=status.HTTP_400_BAD_REQUEST, msg=Messages.IT)
    
    # Verify the token
    id_info = verify_google_token(id_token_str)
    logging.info(id_info)
    if id_info:
        # Extract user information
        logging.info("ID token payload: %s", id_info)
        email = id_info.get('email')
        name = id_info.get('name', '')
        profile_picture = id_info.get('picture', '')
        logging.info("User data extracted: email=%s, name=%s", email, name)
        
       
        
        # Handle user creation or login
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'email': email,  # Corrected field name
                'name': name,  # Corrected field name
                'profile_picture': profile_picture,  # Corrected field picture
                'email_verified': True,
            }
        )
        
        if created:
            logging.info("New user created: email=%s", email)
        else:
            logging.info("Existing user logged in: email=%s", email)
        
        # Generate token or session for the user
        # For example, create a Django session or JWT token
        
        return {'email': user.email, 'name': user.name}
    
    logging.error("Invalid token provided.")
    return echo(status=status.HTTP_400_BAD_REQUEST, msg=Messages.IT)
