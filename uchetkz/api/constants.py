FORGOT_PASSWORD_MESSAGE = 'To change password follow by link below ' \
						'with POST method and with body "password" and "confirm_password" \n' \
						'http://localhost:8000/api/auth/change/password/{user_pk}/{random_string}/ \n' \
						'NOTE: lifetime of this link is {lifetime} seconds'

FORGOT_PASSWORD_TOKEN_EXPIRE = "Link by followed has expired"
