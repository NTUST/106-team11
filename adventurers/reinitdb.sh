#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo 'remove files related to sqlite in django...'
rm -v */migrations/000*
rm db.sqlite3

source env/bin/activate
python manage.py makemigrations
python manage.py migrate

python gen_data.py

echo ''
echo 'Setup super user...'
python manage.py createsuperuser --email=admin@test.local

echo ''
echo 'Running development server...'
python manage.py runserver
exit 0
