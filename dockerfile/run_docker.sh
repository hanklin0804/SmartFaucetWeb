#! /bin/bash

export DOCKER_IMAGE_NAME='backend'
export DOCKER_CONTAINER_NAME='backend'
sudo docker run -ti -p port:port --name $DOCKER_CONTAINER_NAME $DOCKER_IMAGE_NAME