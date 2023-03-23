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
docker pull mongo
docker run -d -p 27017:27017 -v /home/hanklin0804/SmartFaucetWeb/database/mongodb_data:/data/db --name mongodb mongo

# ---------啟動mysql服務-------------



