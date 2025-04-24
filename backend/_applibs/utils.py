import logging
import re
from datetime import datetime
# from cryptography.fernet import Fernet
from django.conf import settings
# import pandas as pd
# import pytz
from django.utils import timezone
from orm.choices import InsertChoice
from _applibs.response import echo, Messages
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from html import escape

def get_timezone_based_time(time_zone: str) -> (datetime, str):
    temp = time_zone.split('GMT')[-1]
    target_timezone = pytz.timezone(time_zone)
    if temp.startswith('+'):
        value = int(temp.split('+')[-1])
        current_time = (timezone.localtime() + timezone.timedelta(hours=value * 2)).astimezone(target_timezone)
        current_day = current_time.strftime('%A')
    else:
        value = int(temp.split('-')[-1])
        current_time = (timezone.localtime() - timezone.timedelta(hours=value * 2)).astimezone(target_timezone)
        current_day = current_time.strftime('%A')

    return current_time, current_day

def get_first_error(serializer):
    first_error = next(iter(serializer.errors.values()))[0]
    return first_error

def returnIfUserExistAndUnverfied(email):
        from orm.models import User
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            if not existing_user.email_verified:
                return True
            
def returnIfUserExistAndNotSubscribed(email):
        from orm.models import User
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            if not existing_user.is_subscribed:
                return True            
                 
            


