from typing import Optional
from rest_framework.response import Response


class Messages:
    SUCCESS = 'Operation successful'
    CREATED = 'Resource created successfully'
    UPDATED = 'Resource updated successfully'
    DELETED = 'Resource deleted successfully'
    ID = 'Invalid data provided'
    IT = 'Invalid token provided'
    AE = 'Resource already exists'
    NF = 'Resource not found'
    EXCEPTION = 'An exception occurred'
    UNAUTH = 'Unauthenticated access'
    INVALID_PARAMETERS = 'Invalid parameters provided'
    ERROR = 'An unexpected error occurred'
    PERMISSION_DENIED = 'Permission denied'
    NOT_ALLOWED = 'Action not allowed'
    EMAIL_ALREADY_REGISTERED = 'Email is already registered'
    PASSWORD_TOO_WEAK = 'Password is too weak'
    INVALID_DATA = 'The provided data is not valid'


def echo(status: int, msg: str, data: Optional[dict] = None):
    res_data = {'message': msg}
    if data is not None:
        res_data['data'] = data
    return Response(data=res_data, status=status)
