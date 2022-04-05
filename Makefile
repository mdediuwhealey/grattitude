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

open-browser:
	python3 manage.py runserver

serve: serve-setup open-browser
