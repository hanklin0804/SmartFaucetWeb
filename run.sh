# ! /bin/bash/
pipenv --python 3.9.10
# pipenv install -r ./backend/requirements.txt
pipenv install django

sudo docker-compose down
sudo rm -rf ./mysql_data/

sudo rm -rf ./backend/api/devices/migrations/*
sudo rm -rf ./backend/api/accounts/migrations/*

touch ./backend/api/devices/migrations/__init__.py
touch ./backend/api/accounts/migrations/__init__.py



pipenv run python ./backend/manage.py makemigrations

sudo docker-compose up --build