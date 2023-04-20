#----------建立腳色-------------------
sudo adduser --force-badname Flaky
sudo adduser --force-badname Woody
sudo adduser --force-badname Hanklin
sudo usermod -aG sudo Flaky
sudo usermod -aG sudo Woody
sudo usermod -aG sudo Hanklin

#-----------個別建立金要---------------
mkdir ~/.ssh
touch ~/.ssh/authorized_keys
sudo vim ~/.ssh/authorized_keys




sudo apt update -y
sudo apt upgrade -y

# ----------安裝docker-----------------
sudo apt-get update
# 安装必要的软件包，以便apt可以通过HTTPS使用Docker仓库：
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
# 添加Docker官方GPG密钥：
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# 添加Docker APT仓库：
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 啟動Docker服務
sudo systemctl start docker
sudo systemctl enable docker
# 確認docker版本
docker --version
sudo usermod -aG docker $USER
sudo reboot

# -------安裝docker compose--------
sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
docker-compose --version


#-----------看情況安裝--------------
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# ----------.env權限-------------
chmod 600 .env


#-----------安裝Pip pipenv----------
sudo apt update
sudo apt install python3-pip -y
pip3 --version
python3 -m pip install pipenv
vim ~/.bashrc
export PATH="$PATH:/home/$USER/.local/bin"
# export PATH="$PATH:/home/$USER/.local/bin"




