from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authlib.integrations.django_client import OAuth

oauth = OAuth()

# Google Configuration
oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    client_kwargs={'scope': 'openid email profile'},
)

class GoogleLoginAPIView(APIView):
    def get(self, request):
        redirect_uri = 'http://localhost:8000/api/google/callback/'
        return oauth.google.authorize_redirect(request, redirect_uri)


class GoogleCallbackAPIView(APIView):
    def get(self, request):
        token = oauth.google.authorize_access_token(request)
        user_info = oauth.google.parse_id_token(request, token)
        return Response({'user': user_info}, status=status.HTTP_200_OK)
