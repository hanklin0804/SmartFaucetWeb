#!/bin/bash


python manage.py migrate 
python manage.py makemigrations 

# python manage.py loaddata --app api/accounts api/accounts/fixtures/initial_default_data.json
# python manage.py loaddata  api/accounts/fixtures/initial_default_data.json
# python manage.py flush 
python manage.py loaddata  --app accounts initial_default_data.json
python manage.py loaddata  --app devices initial_rpi_data.json
python manage.py loaddata  --app devices initial_tap_data.json
exec python manage.py runserver 0.0.0.0:8787