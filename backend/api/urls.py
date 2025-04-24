from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.google_oauth import GoogleLoginAPIView, GoogleCallbackAPIView
from api.views.users import UserAPIView
from api.views.stripe import CreateCheckoutSessionView 
from api.views.authentication import (
    UserLogoutView,TokenRefreshView,
    UserView,GoogleLoginApi)
from webhooks.stripe import StripeWebhookView

urlpatterns = [

    # User CRUD
    path('users', UserAPIView.as_view(), name='user_list'),
    path('users/<int:user_id>', UserAPIView.as_view(), name='user_detail'),

    # Authentication apis
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/google', GoogleLoginApi.as_view(), name='reset_password'),
    path('auth/user', UserView.as_view(), name='user_view'),
    path('auth/logout', UserLogoutView.as_view(), name='user_logout'),
  
    #stripe 
    path('stripe/create-payment-intent', CreateCheckoutSessionView.as_view(), name='create-payment-intent'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='confirm-payment'),

]

# Serve media files in development
# if settings.DEBUG:
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
