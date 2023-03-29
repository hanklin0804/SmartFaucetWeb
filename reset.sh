#! /bin/bash
sudo docker stop mysql phpmyadmin
sudo docker rm mysql phpmyadmin 

pipenv --rm 