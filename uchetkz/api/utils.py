from random import choice
from string import ascii_lowercase, digits


from django.contrib.auth.models import User


def authenticate(email, password):
	try:
		user = User.objects.get(email=email)
		return user if user.check_password(password) else None
	except User.DoesNotExist:
		return None


def get_user_by_email(email):
	try:
		user = User.objects.get(email=email)
		return user
	except User.DoesNotExist:
		return None


def generate_random_string(length=16, chars=ascii_lowercase+digits, split=4, delimer='-'):

	rand_string = ''.join([choice(chars) for i in range(length)])

	if split:
		token = delimer.join([rand_string[start:start+split] for start in range(0, len(rand_string), split)])

	return rand_string
