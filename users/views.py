from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegisterSerializer, 
                          LoginSerializer, 
                          ForgotPasswordSerializer, 
                          ResetPasswordSerializer, 
                          ChangePasswordSerializer
                    )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .utils import (send_verification_email, 
                    send_welcome_email, 
                    send_password_reset_email, 
                    send_password_change_confirmation_email
                )
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.throttling import AnonRateThrottle
from django.utils import timezone

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        uidb64 = request.GET.get("uid")
        token = request.GET.get("token")

        # Validate UID and token presence
        if not uidb64 or not token:
            return Response({"error": "Missing UID or token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode UID from base64
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Check if the token is valid for the user
            if default_token_generator.check_token(user, token):
                # Check if the token has expired
                if user.verification_token_expiry and timezone.now() > user.verification_token_expiry:
                    return Response({"error": "Verification token has expired."}, status=status.HTTP_400_BAD_REQUEST)

                # If the token is valid and not expired, mark user as active and email verified
                if not user.is_active or not user.is_email_verified:
                    user.is_email_verified = True
                    user.is_active = True
                    user.save()

                    # Send welcome email after successful verification
                    send_welcome_email(user)
                    return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

                # If already verified, return a success message
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

            else:
                # Invalid or expired token
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError):
            # Handle issues with the UID decoding or invalid user ID
            return Response({"error": "Invalid UID or token."}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            # Handle case when no user is found with the provided UID
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        email = request.data.get('email')

        # Check if email is provided in the request
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            if user.is_active and user.is_email_verified:
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

            elif not user.is_active:
                return Response({"message": "Account is not active. Please activate your account."}, status=status.HTTP_400_BAD_REQUEST)

            elif not user.is_email_verified:
                send_verification_email(user)
                return Response({"message": "Your Email is not Verified. Verification email sent."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordView(generics.GenericAPIView):
    """
    View to handle forgot password requests by sending a password reset email.
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        

class ResetPasswordView(generics.GenericAPIView):
    """
    View to handle password reset after the user clicks on the link sent via email.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            # Decode UID and retrieve user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Check if token is valid
            if default_token_generator.check_token(user, token):
                # Check if the token has expired
                if user.verification_token_expiry and timezone.now() > user.verification_token_expiry:
                    return Response({"detail": "Password reset token has expired."}, status=status.HTTP_400_BAD_REQUEST)

                # If token is valid and not expired, reset the password
                user.set_password(new_password)
                user.save()

                # Send confirmation email
                send_password_change_confirmation_email(user)

                return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError):
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user


        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']

            if not user.check_password(old_password):
                return Response({"old_password": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Send confirmation email
            send_password_change_confirmation_email(user)

            # Optional: Invalidate refresh token if provided
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception:
                    raise AuthenticationFailed("Invalid refresh token")

            return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)