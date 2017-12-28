#!/bin/sh

# wait for PSQL server to start
#sleep 10

# cd myproject

# prepare init migration
#su -m myuser -c "python manage.py makemigrations"
python manage.py makemigrations

# migrate db, so we have the latest db schema
#su -m myuser -c "python manage.py migrate"
python manage.py migrate

celery -A django_crawler worker --app=django_crawler.celery_config:app -l debug &

celery -A django_crawler beat --app=django_crawler.celery_config:app -l debug &

# start development server on public ip interface, on port 8000
#su -m myuser -c "python manage.py runserver 0.0.0.0:8000"
#python manage.py runserver 0.0.0.0:8000 &
gunicorn django_crawler.wsgi -b 0.0.0.0:8000 &

tail -f django.log
