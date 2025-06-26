from django.urls import path

from .views import (
    signup_view,
    login_view,
    verify_email,
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
    # Legacy views (optional if not used)
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),

    # Core auth APIs
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-verify-email/', ResendEmailVerificationView.as_view(), name='resend-verification'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Google OAuth2 login
    path('api/google-login/', GoogleLoginView.as_view(), name='google-login'),

    # Password reset
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]


