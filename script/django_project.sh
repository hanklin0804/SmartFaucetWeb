#! /bin/bash

while true; do 
    echo "PROJECT_NAME":
    read PROJECT_NAME
    if [ "$PROJECT_NAME" != "" ]; then
        echo "PROJECT_NAME is $PROJECT_NAME"
        break
    fi
done

django-admin startproject $PROJECT_NAME 
cd $PROJECT_NAME
mkdir api
cd api

while true; do 
    echo "APP_NAME":
    read APP_NAME
    if [ "$APP_NAME" = "quit" ]; then
        break
    elif [ "$APP_NAME" = "" ]; then
        continue
    fi
    echo "APP_NAME is $APP_NAME"
    python ../manage.py startapp $APP_NAME
    touch $APP_NAME/urls.py
    touch $APP_NAME/serializers.py

done


cd ..
tree