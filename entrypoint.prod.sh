#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 1
    done

    echo "Postgres started"
fi

exec "$@"

python manage.py collectstatic --no-input --clear --settings=$DJANGO_SETTINGS_MODULE
python manage.py migrate --no-input --settings=$DJANGO_SETTINGS_MODULE

exec "$@"
