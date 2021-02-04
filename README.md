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

	1) Login And Get Authoriation Token
	Method: POST
	URL: http://localhost:8000/api/auth/

	2) Forgot password. Send message to email with token and link
		Token will store on REDIS CACHE by 120 seconds
	Method: POST
	URL: http://localhost:8000/api/auth/forgot/password/

	3) Change Password with body
		{"password": "pwd", "confirm_password": "pwd"} 
	Method: POST
	URL: http://localhost:8000/api/auth/change/password/<user_pk>/<token>/
	
	(All methods below need Header as "Authentication : Token <token>" for authentication)

	4) Logout
	Method: POST
	URL: http://localhost:8000/api/auth/logout/

	5) Get list of all tasks
	Method: GET
	URL: http://localhost:8000/api/todo/

	6) Get task by task_id
	Method: GET
	URL: http://localhost:8000/api/todo/<task_id>/

	7) Create a new task with by default "is_executed = False" and with body 
		{
		    "title": "Some Title",
		    "description": "This task for creating CRUD operations",
		    "execution_date": "2020-12-12 12:00:00"
		}
	Method: POST
	URL: http://loalhost:8000/api/todo/

	8) Update task by id with body
		{
			"title": "Another Some Task"
		}
	Method: PATCH
	URL: http://localhost:8000/api/todo/<task_id>/

	9) Delete Task by task_id
	Method: DELETE
	URL: http://localhost:8000/api/todo/<task_id>/

	10) Toggle execution for task by task_id
		And sms will be send with CELERY BY REDIS
	Method: POST
	URL: http://localhost:8000/api/todo/<task_id>/execute/