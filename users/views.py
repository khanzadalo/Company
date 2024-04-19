from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from users.email import send_email_confirmation, send_email_reset_password, generate_random_code
from users.models import Profile, User, PasswordResetToken, IsAdminUser
from users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, PasswordChangeSerializer, \
    VerifySerializer, PasswordResetSearchUserSerializer, PasswordResetCodeSerializer, PasswordResetNewPasswordSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        send_email_confirmation(user.email)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user_email = get_object_or_404(User, email=email)
        user = authenticate(request, username=user_email.username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "refresh_token": str(refresh),
                    "access_token": str(access),
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'username or password incorrect!'})

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class ProfileUserAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)


class ChangePasswordView(CreateAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {"error": "New password should not match old password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password successfully changed."}, status=status.HTTP_200_OK
        )


class VerifyOTP(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data.get("otp")

        user = User.objects.filter(otp=otp).first()

        if not user:
            return Response({"error": "User with this confirmation code was not found."}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.otp = None
        user.save()

        return Response({"message": "Account has been successfully verified."}, status=status.HTTP_200_OK)


class ResetPasswordSendEmail(CreateAPIView):
    serializer_class = PasswordResetSearchUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with provided email address not found."},
                            status=status.HTTP_404_NOT_FOUND)

        time = timezone.now() + timezone.timedelta(minutes=5)
        code = generate_random_code()

        password_reset_token = PasswordResetToken(user=user, code=code, time=time)
        password_reset_token.save()

        send_email_reset_password(user.email, code)

        return Response({"detail": "send"}, status=status.HTTP_200_OK)


class PasswordResetCode(CreateAPIView):
    serializer_class = PasswordResetCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        try:
            PasswordResetToken.objects.get(code=code, time__gt=timezone.now())
        except ObjectDoesNotExist:
            return Response({"error": "Invalid password reset code or code expiration time has passed."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({"detail": "success", "code": code}, status=status.HTTP_200_OK)


class PasswordResetNewPassword(CreateAPIView):
    serializer_class = PasswordResetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = kwargs["code"]
        password = serializer.validated_data["password"]

        try:
            password_reset_token = PasswordResetToken.objects.get(code=code, time__gt=timezone.now())
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Invalid password reset code or code expiration time has passed."},
                            status=status.HTTP_404_NOT_FOUND)

        user = password_reset_token.user
        user.set_password(password)
        user.save()

        password_reset_token.delete()

        return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
