!#/bin/bash
apt-get install emacs
export  DEBIAN_FRONTEND=noninteractive 
sudo apt-get install keyboard-configuration
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
sudo rm /etc/alternatives/cuda
sudo ln -s  /usr/local/cuda-12.4 /etc/alternatives/cuda
nvcc --version 
