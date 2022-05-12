import os
import re
import csv
import subprocess
from tabnanny import verbose
# from tkinter import Frame
from scapy.layers.l2 import ARP, Ether
from WifiAdapter import *
import Deauthenticate
import Attack
from scapy import all as sc
import time
from threading import Thread


tmp = []
AllAvialableNetworks = []
DuplicateNetworks = []
NonDuplicateNetworks = []
Dups = []
Clients = []
DefenceNetMA = ""

def WifiSniffingHandler(packet):
    #if packet end with 11 like 802.11
    if packet.haslayer(sc.Dot11):
        #type -menegment subtype-beacon
        if packet.type==0 and packet.subtype==8:
           if packet.addr2 not in tmp:
                AllAvialableNetworks.append(packet)
                tmp.append(packet.addr2)



def FindDuplicateNetworks(Wifiadapter):
    print("\nScanning for malicious wireless netwroks...\n")
    #  iface = the interfaces that we would like to sniff on
    # prn = allows us to pass a function that executes with each packet sniffed
    for ch in range (1,14):
        c = str(ch)
        cmd = "sudo iwconfig "+WifiAdapter+" channel "+ c
        os.system(cmd)
        sc.sniff(iface=Wifiadapter, prn=WifiSniffingHandler , timeout = 5)
    # index = 0
    for net in AllAvialableNetworks:
        # print("{index} - SSID : {net.info} Mac address : {net.addr2}")
        if net.info in NonDuplicateNetworks:
            DuplicateNetworks.append(net.info)
        else:
            NonDuplicateNetworks.append(net.info)
    for net in AllAvialableNetworks:
        if net.info in DuplicateNetworks:
            Dups.append(net)


def DisconnectAll(network , Wifiadapter):
    Frames = []
    for ma in Clients:
        dot11 = sc.Dot11(addr1=ma, addr2=network.addr2, addr3=network.addr2)
        frame = sc.RadioTap()/dot11/sc.Dot11Deauth(reason=7)
        Frames.append(frame)
    while True:
        for ch in range (1,14):
            for fr in Frames:
                c = str(ch)
                cmd = "sudo iwconfig "+WifiAdapter+" channel "+ c
                os.system(cmd)    
                sc.sendp(fr, iface=Wifiadapter, inter=0.100 , verbose = 0)

    return 0



def FindClient(net , WifiAdapter):
    print("\nScanning for clients...\n")
    # sniff packets with WifiAdapter and calls to handler function for each packet , 
    # to find out who are the clients that connected to the chosen wifi network 
    for ch in range (1,14):
        c = str(ch)
        cmd = "sudo iwconfig "+WifiAdapter+" channel "+ c
        os.system(cmd)
        sc.sniff(iface=WifiAdapter, prn=FindClientHandler , timeout = 5)
    print("\n\n\nThe Clients who connected to the chosen wifi are:\n")

def FindClientHandler(pkt):
    stamgmtstypes = (0, 2, 4)
    # Make sure the packet has the Scapy Dot11 layer present
    if pkt.haslayer(sc.Dot11):
        if pkt.subtype in stamgmtstypes:
            if pkt.addr3 == DefenceNetMA and pkt.addr2 not in Clients and pkt.addr2 != DefenceNetMA:
                Clients.append(pkt.addr2)


if __name__ == "__main__":

    #finding wifi adapter
    WifiAdapter = WifiAdapterFinder()
    #changing adapter to monitor mode
    MonitorMode(WifiAdapter)
    FindDuplicateNetworks(WifiAdapter)
    print("The possible malicious networks are : ")
    index = 0
    for net in Dups:
        print(f"{index} - SSID : {net.info} Mac address : {net.addr2}")
        index +=1
    while True:
            net_index = input("\nPlease select the Wifi network you want to defence from : ")
            try:
                if Dups[int(net_index)]:
                    break
            except:
                print("Please enter a number that corresponds with the choices available.")
    DefenceNetMA = Dups[int(net_index)].addr2
    FindClient(Dups[int(net_index)] , WifiAdapter)
    print("\n clinets : ")
    for cl in Clients:
        print(cl)
    print("\n Disconnecting al users from the malicious network..\n")
    DisconnectAll(Dups[int(net_index)] , WifiAdapter)
    