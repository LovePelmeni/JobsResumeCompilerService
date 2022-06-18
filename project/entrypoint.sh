#!/bin/sh

echo "Running Application."
python manage.py makemigrations && python manage.py migrate && \
python manage.py test main.tests && python manage.py collectstatic --no-input && \
gunicorn API.API.wsgi:application --bind 0.0.0.0 --port 8000 --workers 5 --timeout 100




