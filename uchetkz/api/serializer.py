from rest_framework import serializers
from .utils import authenticate, get_user_by_email
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(write_only=True)
	password = serializers.CharField(max_length=128, write_only=True)

	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, attrs):
		email = attrs.get('email', None)
		password = attrs.get('password', None)

		if email is None:
			raise serializers.ValidationError('Email is required')

		if password is None:
			raise serializers.ValidationError('Password is required')

		user = authenticate(email, password)

		if user is None:
			raise serializers.ValidationError('User not found')

		token, created = Token.objects.get_or_create(user=user)

		return {
			'token': token
		}


class EmailSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate(self, attrs):
		email = attrs.get('email', None)

		if email is None:
			raise serializers.ValidationError('Email is required')

		if get_user_by_email(email) is None:
			raise serializers.ValidationError('User not found')

		return attrs


class ChangePasswordSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=120)
	confirm_password = serializers.CharField(max_length=120)

	def validate(self, attrs):
		password = attrs.get('password', None)
		confirm_password = attrs.get('confirm_password', None)

		if password is None:
			raise serializers.ValidationError('Enter new password')
		elif len(password) <= 6:
			raise serializers.ValidationError('Password must contain 7 or more characters')

		if confirm_password is None:
			raise serializers.ValidationError('Enter confirmation password')

		if confirm_password != password:
			raise serializers.ValidationError('Passwords are not same')

		return attrs
