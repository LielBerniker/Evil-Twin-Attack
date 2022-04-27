import os
import re
import csv
import subprocess
# import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
import WifiAdapter as WAF
import Twin_create as TC
import search_victim as SV
from scapy import all as sc
import time

AvialableWifiNetworks = []
def PacketHendler(packet):
    if packet.haslayer(sc.Dot11):
        #type -menegment subtype-beacon
        if packet.type==0 and packet.subtype==8:
            #address 2 - transmitter.
            exist = False
            for pkt in AvialableWifiNetworks:
                if packet.addr2 == pkt.addr2:
                    exist = True
            if not exist:
                AvialableWifiNetworks.append(packet)
                print("Access Point Mac: %s with SSID:%s" %(packet.addr2 ,packet.info))

def WifiNetworksFinder(hacknic):
    start_time = time.time()
    seconds = 10
    sc.sniff(iface=hacknic,prn = PacketHendler , timeout = 10)
    print("\n\n\nThe Avialable Wifi Netwroks are:")
    for index, item in enumerate(AvialableWifiNetworks):
        print(f"{index} - SSID : {item.info} , MAC Address : {item.addr2}")
    while True:
        wifi_network_choice = input("Please select the Wifi network you want to use for the attack: ")
        try:
            if AvialableWifiNetworks[int(wifi_network_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")
    return AvialableWifiNetworks[int(wifi_network_choice)].addr2


if __name__ == "__main__":
    hacknic = WAF.WifiAdapterFinder()
    WAF.MonitorMode(hacknic)
    chosen_network = WifiNetworksFinder(hacknic)
    print("The chosen wifi is " , chosen_network) 
    # SV.find_all_users_in_network(WifiNetworksFinder(chosen_network))

