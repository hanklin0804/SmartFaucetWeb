# ! /bin/bash/

sudo docker-compose down
sudo rm -rf ./mysql_data/

sudo rm -rf ./backend/api/devices/migrations/*
sudo rm -rf ./backend/api/accounts/migrations/*

touch ./backend/api/devices/migrations/__init__.py
touch ./backend/api/accounts/migrations/__init__.py



python ./backend/manage.py makemigrations

sudo docker-compose up --build