from rest_framework import serializers
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

	class Meta:
		model = Task
		fields = (
			'pk',
			'title',
			'description',
			'execution_date',
			'is_executed'
		)
		read_only_fields = ('pk',)
