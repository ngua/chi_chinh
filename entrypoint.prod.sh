#!/bin/bash

python manage.py collectstatic --no-input --clear --settings=$DJANGO_SETTINGS_MODULE
python manage.py migrate --no-input --settings=$DJANGO_SETTINGS_MODULE

exec "$@"
