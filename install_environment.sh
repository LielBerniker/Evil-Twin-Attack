#!/bin/sh


echo Perform Evil Twin attack requirements
sudo apt-get update
sudo apt install apache2
sudo apt install hostapd
sudo apt install dnsmaskq
sudo apt install python3-scapy
sudo pip install colorama
sudo apt install net-tools
echo installing all requirements is finished