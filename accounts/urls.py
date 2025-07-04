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
    SendOTPView,
    VerifyOTPView,
)

urlpatterns = [
    #auth APIs
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-verify-email/', ResendEmailVerificationView.as_view(), name='resend-verification'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Google OAuth2 login
    path("api/google-login/", GoogleLoginView.as_view(), name="google-login"),

    # Password reset
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),


    #Login using phone otp
    path("api/login-phoneno/", SendOTPView.as_view(), name="login-otp"),
    path("api/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

]


