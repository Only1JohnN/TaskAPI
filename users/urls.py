from django.urls import path
from .views import (RegisterView, 
                    LoginView, 
                    LogoutView, 
                    VerifyEmailView, 
                    ResendVerificationEmailView, 
                    ForgotPasswordView, 
                    ResetPasswordView, 
                    ChangePasswordView
                )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
    
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]
