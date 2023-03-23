# 刪除所有 container
docker rm -f $(docker ps -aq)

# 刪除所有 image
docker rmi -f $(docker images -aq)
