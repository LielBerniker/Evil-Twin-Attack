import os
import re
import csv
import subprocess
# import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
import WifiAdapter as WAF
import Twin_create as TC
from scapy import all as sc
import time

AvialableWifiNetworks = []
Clients = []
ChosenWifiMA = ""
def PacketHendler(packet):
    #if packet end with 11 like 802.11
    if packet.haslayer(sc.Dot11):
        #type -menegment subtype-beacon
        if packet.type==0 and packet.subtype==8:
            #address 2 - transmitter.
            exist = False
            # add the packet to AvialableWifiNetworks if not already in
            for pkt in AvialableWifiNetworks:
                if packet.addr2 == pkt.addr2:
                    exist = True
            if not exist:
                AvialableWifiNetworks.append(packet)
                print("Access Point Mac: %s with SSID:%s" %(packet.addr2 ,packet.info))

#  hacknic = selected interface
def WifiNetworksFinder(hacknic):
    start_time = time.time()
    seconds = 10
    #  iface = the interfaces that we would like to sniff on
    # prn = allows us to pass a function that executes with each packet sniffed
    sc.sniff(iface=hacknic, prn=PacketHendler , timeout = 10)

    # printing the Available Wifi Networks withe their ssid(name) and their mac address
    print("\n\n\nThe Available Wifi Networks are:")
    for index, item in enumerate(AvialableWifiNetworks):
        print(f"{index} - SSID : {item.info} , MAC Address : {item.addr2} ,")
    
    while True:
        wifi_network_choice = input("Please select the Wifi network you want to use for the attack: ")
        try:
            if AvialableWifiNetworks[int(wifi_network_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")
    return AvialableWifiNetworks[int(wifi_network_choice)].addr2

def CLientsSniffing(pkt):
    stamgmtstypes = (0, 2, 4)
    # Make sure the packet has the Scapy Dot11 layer present
    if pkt.haslayer(sc.Dot11):
        # Check to make sure this is a management frame (type=0) and that
        # the subtype is one of our management frame subtypes indicating a
        # a wireless client
        if pkt.type == 0 and pkt.subtype in stamgmtstypes:
            if (pkt.addr1 == ChosenWifiMA or pkt.addr3 == ChosenWifiMA or pkt.addr3 == ChosenWifiMA):
                if pkt.addr2 not in Clients:
                    Clients.append(pkt.addr1)

def ClientsFinder(hacknic):
    sc.sniff(iface=hacknic, prn=CLientsSniffing , timeout = 30)


if __name__ == "__main__":
    hacknic = WAF.WifiAdapterFinder()
    WAF.MonitorMode(hacknic)
    ChosenWifiMA = WifiNetworksFinder(hacknic)
    ClientsFinder(hacknic)
    for addr in Clients:
        print(addr)
    # print("The chosen wifi is : %s" , WifiNetworksFinder(hacknic))
    # SN.




# # IFACE = WAF.WifiAdapterFinder()
# # IFACE_NAME = WAF.MonitorMode(IFACE)
# iface = "wlan0mon"
# devices = set()
# def PacketHandler(pkt):
#     print("packet found")
#     if pkt.haslayer(Dot11):
#         dot11_layer = pkt.getlayer(Dot11)
#         print("packet has layer dot11")  
#         if dot11_layer.addr2 and (dot11_layer.addr2 not in devices):
#             devices.add(dot11_layer.addr2)
#             print((len(devices) -1 ), dot11_layer.addr2, dot11_layer.payload.name)
  
  
# sniff(iface=iface,prn=PacketHandler)