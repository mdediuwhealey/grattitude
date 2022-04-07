.PHONY: venv install serve-setup open-browser serve
venv:
	python3 -m venv venv; \

install: venv
	source ./venv/bin/activate; \
	pip3 install -r requirements.txt;

serve-setup:
	python3 manage.py db upgrade;

migrate-start: 
	python3 manage.py db migrate -m "start"

runserver:
	python3 manage.py runserver

run-intros:
	python3 manage.py intros

runs-reminders:
	python3 manage.py reminders


serve: serve-setup runserver
