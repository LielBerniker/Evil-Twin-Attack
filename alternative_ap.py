import os
import re
import csv
import sys
import subprocess
# import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
from WifiAdapter import WifiAdapterFinder
from WifiAdapter import MonitorMode
import Deauthenticate
import Twin_create
from scapy import all as sc
import time
from threading import Thread 
from string import Template

WifiAdapter = ""
def change_template(path):
    with open(path, 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(INTERFACE=WifiAdapter))
        f.truncate()

def prepare_fake_access_point():
    """
    prepare the environment setup for creating the fake access point
    :param access_point_bssid represent the network name
    """
    os.system('rm -rf build/')
    os.system('cp -r configuration_files build_up')
    change_template('build_up/hostapd.conf')
    change_template('build_up/dnsmasq.conf')
    change_template('build_up/prepare_ap.sh')
    change_template('build_up/reboot.sh')
    print("finish prepare conf files")
    os.system('sudo sh build_up/prepare_ap.sh')

if __name__ == "__main__":

    #finding wifi adapter
    # WifiAdapter = WifiAdapterFinder()
    #changing adapter to monitor mode
    # MonitorMode(WifiAdapter)
    #scanning for wifi network to attack
    # prepare_fake_access_point()
    # time.sleep(120)
    os.system('sudo sh configuration_files/reboot.sh')



