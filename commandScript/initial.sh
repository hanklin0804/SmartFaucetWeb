#!/bin/bash

# 创建用户
sudo adduser --force-badname Flaky
sudo adduser --force-badname Woody
sudo adduser --force-badname Hanklin

# 将用户添加到sudo用户组
sudo usermod -aG sudo Flaky
sudo usermod -aG sudo Woody
sudo usermod -aG sudo Hanklin

# 创建SSH目录和authorized_keys文件
mkdir ~/.ssh
touch ~/.ssh/authorized_keys

# 更新Ubuntu
sudo apt update -y && sudo apt upgrade -y

# 安装Docker
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 确认docker版本
docker --version

# 将当前用户添加到docker用户组
sudo usermod -aG docker $USER


# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose

# 确认docker-compose版本
docker-compose --version

# 安装Pip和Pipenv
sudo apt update
sudo apt install python3-pip -y
pip3 --version
python3 -m pip install pipenv

# 更新bashrc以添加pipenv到PATH
echo 'export PATH="$PATH:/home/$USER/.local/bin"' >> ~/.bashrc
source ~/.bashrc

# 重启系统以使用户组更改生效
sudo reboot
