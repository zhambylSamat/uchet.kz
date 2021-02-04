from django.urls import path
from .views import (TaskView, TaskDetailView, TaskActionView)

urlpatterns = [
	path('', TaskView.as_view()),
	path('<task_id>/', TaskDetailView.as_view()),
	path('<task_id>/execute/', TaskActionView.as_view())
]
