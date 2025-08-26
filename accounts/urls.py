from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    UserProfileView,
    GoogleLoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ResendEmailVerificationView, ChangePasswordView, StaffListCreateAPIView, StaffDetailAPIView,AccountSettingsView
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

    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Change password
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),

    # Staff
    path('staffs/',StaffListCreateAPIView.as_view(),name='staff-list-create'),
    path('staffs/<int:pk>/',StaffDetailAPIView.as_view(),name='staff-detail'),

    # Account settings
    path('settings/account/',AccountSettingsView.as_view(),name='account-settings'),
]


