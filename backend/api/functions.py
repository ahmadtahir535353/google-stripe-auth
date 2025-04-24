from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import datetime, timedelta
from orm.models import User
import random
import os, logging

def generateToken(user_id, request):
    """
    Generate JWT tokens with custom expiration and domain handling.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User does not exist")
    
    refresh = RefreshToken.for_user(user)

    refresh.set_exp(lifetime=timedelta(days=1))

    host = request.get_host()
    domain_parts = host.split('.')
    main_domain = ''
    if len(domain_parts) >= 2:
        main_domain = '.' + '.'.join(domain_parts[-2:])  # .example.com
    subdomain = "*"

    refresh['domain'] = main_domain
    refresh['subdomain'] = subdomain

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        'access': access_token,
        'refresh': refresh_token
    }


def generate_unique_filename(original_filename):
    """
    Generate a unique filename with a timestamp.
    """
    base, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{base}_{timestamp}{ext}"
    return unique_filename