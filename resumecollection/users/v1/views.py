import logging

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import RedirectView
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from resumecollection.users.helpers import UpdatePasswordHelper
from resumecollection.users.v1.serializers import (
    UserSerializer,
    ForgotPasswordEmailSerializer,
    UpdatePasswordRequestSerializer,
    LoginRequestSerializer,
)
from resumecollection.utils.authentication import create_login_token
from resumecollection.utils.email import send_password_update_email
from resumecollection.utils.permissions import UpdatePasswordPermission
from resumecollection.utils.response_handler import validation_exception_handler

logger = logging.getLogger(__name__)

User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class ForgotPasswordAPIView(APIView):
    def validate_email(self, query_params):
        serializer = ForgotPasswordEmailSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get("email")

    def get(self, request) -> Response:
        try:
            user_email_address = self.validate_email(request.query_params)
            user = get_object_or_404(User, email=user_email_address)
            send_password_update_email(
                user, UpdatePasswordHelper.generate_update_password_url(user)
            )
        except Http404:
            logger.error(
                f"Failure to find the object, the User with the email "
                f"{user_email_address} doesnt exist"
            )
            return Response(
                data=f"The User with the email {user_email_address} doesnt exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as validation_error:
            logger.error(
                f"Validation error occurred while sending forget password email. "
                f"Error: {validation_error}"
            )
            return Response(
                data="The email address is not valid",
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info(
            f"Email for updating password has been sent to {user_email_address}"
        )
        return Response(
            data="Email has been sent successfully", status=status.HTTP_200_OK
        )


class UpdateUserPasswordAPIView(APIView):
    permission_classes = [UpdatePasswordPermission]

    def get_permissions(self):
        if self.request.data.get("is_admin"):
            return [permissions.IsAuthenticated()]
        return super(UpdateUserPasswordAPIView, self).get_permissions()

    def post(self, request) -> Response:
        try:
            serialized_data = UpdatePasswordRequestSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=request.data.get("email"))
            user.set_password(serialized_data.data["confirm_password"])
            user.save()
            UpdatePasswordHelper.invalidate_update_password_token(user.email)
            return Response(
                data="Password has been updated successfully", status=status.HTTP_200_OK
            )
        except Http404:
            logger.error(f"Failure to find the object, user with email doesnt exist")
            return Response(
                data="The User doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as validation_error:
            logger.error(
                f"Validation error occurred while updating the password with {validation_error}"
            )
            return Response(
                data=f"Failed to update the password with {validation_error}",
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            request_serializer = LoginRequestSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
            username = request_serializer.validated_data["username"]
            password = request_serializer.validated_data["password"]
            remember_me = request_serializer.validated_data["remember_me"]

            user = authenticate(username=username.lower(), password=password)

            if not user:
                return Response(
                    data="Credentials not correct. Unable to Login.",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            token = create_login_token(user, remember_me)
            return Response(
                data={
                    "token": token,
                    "user": UserSerializer(user).data,
                    "message": "Successfully logged in.",
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as error:
            logger.info(
                f"Validation failed for User Login with exception {error}"
            )
            data = validation_exception_handler(error)
            data.update({"message": error.default_detail})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
