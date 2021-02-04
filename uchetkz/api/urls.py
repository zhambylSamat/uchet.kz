from django.urls import path
from .views import LoginApiView, LogOutView, ForgotPasswordView, ChangePasswordView

urlpatterns = [
	path('', LoginApiView.as_view()),
	path('logout/', LogOutView.as_view()),
	path('forgot/password/', ForgotPasswordView.as_view()),
	path('change/password/<user_pk>/<token>/', ChangePasswordView.as_view())
]
