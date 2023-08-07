SHELL := /bin/bash

run:

	source env/bin/activate && env FLASK_APP=app/manage.py python -m flask run

run_me:
	source env/bin/activate && flask --app app/manage.py --debug run