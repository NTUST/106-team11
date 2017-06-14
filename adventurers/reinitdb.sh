#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo 'remove files related to sqlite in django...'
rm -v */migrations/000*
rm -v db.sqlite3

source env/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py ckeck_permissions

python3 gen_data.py

echo
echo 'Setup super user...'
python3 manage.py createsuperuser --email=admin@test.local

echo
echo 'Running development server...'
python3 manage.py runserver
exit 0
