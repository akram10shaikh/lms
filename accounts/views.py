from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import PhoneOTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, GoogleAuthSerializer
from django.contrib.auth import login as django_login

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    TokenSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ResendEmailSerializer
)

User = get_user_model()

# Register + Send Email
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"detail": "Registration successful. Please check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )


# JWT Login + Active Check
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token_serializer = TokenSerializer(context={"user": user})
        tokens = token_serializer.validate({})
        return Response(tokens, status=status.HTTP_200_OK)


# Email Verification Link
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully. You can now login."})
        else:
            return Response({"message": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)


# Protected Profile (JWT Required)
class UserProfileView(generics.RetrieveAPIView):
    #queryset=User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Password Reset Request
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_url = f"http://127.0.0.1:8000/api/password-reset-confirm/{uid}/{token}/"

        send_mail(
            "Reset your password",
            f"Click the link to reset your password:\n{reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent."})


# Password Reset Confirm
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class=PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        password = request.data.get("password")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link."}, status=400)

        if token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset successfully."})
        else:
            return Response({"error": "Invalid or expired token."}, status=400)


# Resend Email Verification
class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class=ResendEmailSerializer

    def post(self, request):
        serializer=ResendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"message": "Email is already verified."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = f"http://127.0.0.1:8000/api/verify-email/{uid}/{token}/"

        send_mail(
            "Verify your email",
            f"Click the link to verify your Account:\n{verify_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Verification email resent successfully."})

# Send otp to user register phone number
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone_number"]

        otp_obj, _ = PhoneOTP.objects.get_or_create(phone_number=phone)
        otp_obj.generate_otp()

        # In real case, send via SMS gateway like Twilio
        print(f"OTP for {phone} is {otp_obj.otp}")

        return Response({"message": "OTP sent successfully."})
# Verify the otp   
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone_number"]
        entered_otp = serializer.validated_data["otp"]

        try:
            otp_obj = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            return Response({"error": "Phone number not found."}, status=404)

        if otp_obj.otp == entered_otp:
            try:
                user = User.objects.get(phone_number=phone)
            except User.DoesNotExist:
                return Response({"error": "User not registered."}, status=404)

            if not user.is_active:
                return Response({"error": "User is not active."}, status=403)

            django_login(request, user)  # For session-based login
            refresh = RefreshToken.for_user(user)  # For JWT
            return Response({
                "message": "Login successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response({"error": "Invalid OTP."}, status=400)
