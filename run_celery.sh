#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd myproject
su -m myuser -c "celery worker -A django_crawler.django_config -Q default -n default@%h"