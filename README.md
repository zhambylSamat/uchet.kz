1) Clone the project from git:
	git clone https://github.com/zhambylSamat/uchet.kz.git

2) Create virtual environment:
	python -m venv venv

3) Activate project:
	.\venv\Scripts\activate

4) Upgrade your pip:
	python -m pip install --upgrade pip

5) Install requirements:
	pip install -r requirements.txt

6) Migrate database (models):
	python manage.py migrate

7) Create superuser:
	python manage.py createsuperuser

8) Install and Run redis-server (from https://redis.io/topics/quickstart)

9) Run celery:
	celery -A uchetkz.celery worker -l info --pool=solo


Urls and its description:
	
	1) POST http://localhost:8000/api/auth/		-> Login And Get Authoriation Token

	2) POST http://localhost:8000/api/auth/forgot/password/		-> Forgot password. Send message to email with token and link
																	Token will store on REDIS CACHE by 120 seconds

	3) POST http://localhost:8000/api/auth/change/password/<user_pk>/<token>/		-> Change Password with body
																						{"password": "pwd", "confirm_password": "pwd"} 

	(All methods below need Header as "Authentication : Token <token>" for authentication)

	4) POST http://localhost:8000/api/auth/logout/		-> Logout

	5) GET http://localhost:8000/api/todo/		-> Get list of all tasks

	6) GET http://localhost:8000/api/todo/<task_id>/		-> Get task by task_id

	7) POST http://loalhost:8000/api/todo/		-> Create a new task with by default "is_executed = False" and with body 
												{
												    "title": "Some Title",
												    "description": "This task for creating CRUD operations",
												    "execution_date": "2020-12-12 12:00:00"
												}

	8) PATCH http://localhost:8000/api/todo/<task_id>/		-> Update task by id with body
															{
																"title": "Another Some Task"
															}

	9) DELETE http://localhost:8000/api/todo/<task_id>/		-> Delete Task by task_id

	10) POST http://localhost:8000/api/todo/<task_id>/execute/		-> Toggle execution for task by task_id
																		And sms will be send with CELERY BY REDIS