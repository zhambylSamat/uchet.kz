from django.db import models


class Task(models.Model):
	title = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(null=False, blank=False)
	execution_date = models.DateTimeField(auto_now_add=False, auto_now=False)
	is_executed = models.BooleanField(default=False)

	class Meta:
		ordering = ['execution_date']

	def __str__(self):
		return '{id}) {title}'.format(id=self.pk, title=self.title)
