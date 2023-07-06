

sudo apt update -y
sudo apt upgrade -y


# ----------專案資料夾------------------
# ----------檔案目錄需要統一------------
cd ~
mkdir database
cd database
mkdir mongodb_data
mkdir mysql_data


# ---------啟動mongoDB服務-------------
docker rm -f mongodb
source .env
docker run -itd -p 27017:27017 -v $MongodbPath:/data/db --name mongodb --restart unless-stopped mongo:latest

# ---------啟動mysql服務-------------
docker rm -f mysql
source .env
docker run -itd --name mysql -e MYSQL_ROOT_PASSWORD=$Mysql_PASSWORD -p 3306:3306 -v $MysqlPath:/var/lib/mysql --restart unless-stopped mysql:latest


# ----------------MQTT-----------------
# broker
docker rm -f broker
docker run -itd --name broker -p 48755:1883 -p 48756:18083 -e EMQX_NAME=emqx -e EMQX_LOG__LEVEL=debug -e EMQX_LOADED_PLUGINS=emqx_recon,emqx_retainer,emqx_management,emqx_dashboard  emqx/emqx
