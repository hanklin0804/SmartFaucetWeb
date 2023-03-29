#! /bin/bash
sudo apt-get install libmysqlclient-dev
pipenv install 
cd project_test/backend
sudo docker run -itd --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 mysql 
sudo docker run --name phpmyadmin -d --link mysql -e PMA_HOST=mysql -p 8080:80 phpmyadmin/phpmyadmin

# pipenv run python manage.py makemigrations
# pipenv run python manage.py migrate
# pipenv run python manage.py runserver 0.0.0.0:8787