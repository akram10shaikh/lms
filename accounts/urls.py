from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    UserProfileView,
    GoogleLoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ResendEmailVerificationView,
)

urlpatterns = [
    #auth APIs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verify-email/', ResendEmailVerificationView.as_view(), name='resend-verify-email'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Google OAuth2 login
    path("google-login/", GoogleLoginView.as_view(), name="google-login"),

    # Password reset
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

]


