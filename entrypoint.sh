#!/bin/sh
if [ "$1" = "run" ]; then
    /usr/sbin/nginx && /usr/local/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock  wsgi:app
fi
if [ "$1" = "intro" ]; then
    python manage.py intros
fi
if [ "$1" = "remind" ]; then
    python manage.py reminders
fi

