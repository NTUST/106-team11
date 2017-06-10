#!/bin/bash

rm -v */migrations/000*
rm db.sqlite3

source env/bin/activate
python manage.py makemigrations
python manage.py migrate

python gen_data.py
exit 0
