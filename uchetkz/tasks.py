from uchetkz.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def sent_task_execution_result(email, is_executed):
	message = 'Status of execution of task is {status}'.format(status=('EXECUTED' if is_executed else 'NOT EXECUTED'))
	send_mail('Task Execution', message, settings.EMAIL_HOST_USER, [email])
