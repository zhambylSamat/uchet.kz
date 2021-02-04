from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializer import LoginSerializer, EmailSerializer, ChangePasswordSerializer
from django.core.cache import cache
from django.conf import settings
from .utils import generate_random_string, get_user_by_email
from django.core.mail import send_mail
from .constants import FORGOT_PASSWORD_MESSAGE, FORGOT_PASSWORD_TOKEN_EXPIRE


class LoginApiView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):

		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=HTTP_200_OK)


class LogOutView(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self, request):
		request.user.auth_token.delete()
		return Response({'message': 'Successfully logged out'}, status=HTTP_200_OK)


class ForgotPasswordView(APIView):

	permission_classes = (AllowAny,)

	@staticmethod
	def post(request):

		serializer = EmailSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = get_user_by_email(serializer.data['email'])
		random_string = generate_random_string()
		cache.set(user.pk, random_string, settings.REDIS_TIMEOUTS['FORGOT_PASSWORD'])

		message = FORGOT_PASSWORD_MESSAGE.format(user_pk=user.pk, random_string=random_string,
												lifetime=settings.REDIS_TIMEOUTS['FORGOT_PASSWORD'])

		send_mail('Change Password', message, settings.EMAIL_HOST_USER, [user.email])
		return Response({'message': 'Check your mail for change your password'})


class ChangePasswordView(APIView):

	permission_classes = (AllowAny,)

	@staticmethod
	def post(request, user_pk, token):
		if user_pk not in cache or cache.get(user_pk) != token:
			return Response(FORGOT_PASSWORD_TOKEN_EXPIRE, status=HTTP_400_BAD_REQUEST)

		change_password_serializer = ChangePasswordSerializer(data=request.data)
		change_password_serializer.is_valid(raise_exception=True)

		try:
			user = User.objects.get(pk=user_pk)
			user.set_password(change_password_serializer.data['password'])
			user.save()
			cache.delete(user_pk)
			return Response(status=HTTP_201_CREATED)
		except User.DoesNotExist:
			return Response(status=HTTP_400_BAD_REQUEST)
