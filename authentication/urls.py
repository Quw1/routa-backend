from django.urls import path
from .views import (
    RegisterAPIView, VerifyEmailAPIView, LoginAPIView, PasswordTokenCheckAPIView, RequestPasswordResetEmailAPIView,
    SetNewPasswordAPIView, LogoutAPIView, GetUserAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmailAPIView.as_view(), name='email-verify'),
    path('get-me/', GetUserAPIView.as_view(), name='get-me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-password-reset/', RequestPasswordResetEmailAPIView.as_view(), name='request-password-reset'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]
