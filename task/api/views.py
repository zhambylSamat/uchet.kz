from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from ..models import Task
from .constants import *
from uchetkz.tasks import sent_task_execution_result


class TaskView(APIView):

	permission_classes = (IsAuthenticated,)

	@staticmethod
	def get(request):
		tasks = Task.objects.all()

		task_serializer = TaskSerializer(tasks, many=True)
		return Response(task_serializer.data, status=HTTP_200_OK)

	@staticmethod
	def post(request):
		task_serializer = TaskSerializer(data=request.data)
		if task_serializer.is_valid():
			task_serializer.save()
			return Response(status=HTTP_201_CREATED)
		return Response(task_serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):

	permission_classes = (IsAuthenticated,)

	@staticmethod
	def get(requset, task_id):
		try:
			task = Task.objects.get(pk=task_id)
			task_serializer = TaskSerializer(task, many=False)
			return Response(task_serializer.data, status=HTTP_200_OK)

		except Task.DoesNotExist:
			return Response({}, status=200)

	@staticmethod
	def patch(request, task_id):
		try:
			task = Task.objects.get(pk=task_id)
			task_serializer = TaskSerializer(task, data=request.data, many=False, partial=True)
			if task_serializer.is_valid():
				task_serializer.save()
				return Response(task_serializer.data, HTTP_201_CREATED)
			return Response(task_serializer.errors, HTTP_400_BAD_REQUEST)
		except Task.DoesNotExist:
			return Response({'error': TASK_BY_ID_DOES_NOT_FOUND.format(task_id=task_id)})

	@staticmethod
	def delete(request, task_id):
		try:
			task = Task.objects.get(pk=task_id)
			task.delete()
			return Response(status=HTTP_204_NO_CONTENT)
		except Task.DoesNotExist:
			return Response({'error': TASK_BY_ID_DOES_NOT_FOUND.format(task_id=task_id)})


class TaskActionView(APIView):

	permission_classes = (IsAuthenticated,)

	@staticmethod
	def post(request, task_id):

		try:
			task = Task.objects.get(pk=task_id)
			task.is_executed = not task.is_executed
			task.save()
			task_serializer = TaskSerializer(task)
			sent_task_execution_result.delay(request.user.email, task.is_executed)
			return Response(task_serializer.data, status=HTTP_201_CREATED)
		except Task.DoesNotExist:
			return Response({'error': TASK_BY_ID_DOES_NOT_FOUND.format(task_id=task_id)})
