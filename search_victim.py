import os
# We require regular expressions.
import re
import csv
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether

def find_all_users_in_network(target_ip):
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    # a list of clients, we will fill this in the upcoming loop
    clients = []
    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    # print clients
    print("Available devices in the network:")
    print("IP" + " " * 18 + "MAC")
    for index, client in clients:
        print(f"{index}" + "{:16}    {}".format(client['ip'], client['mac']))
    while True:
        device_choice = input("Please select the device you want to use for the attack: ")
        try:
            if clients[int(device_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")

        # For easy reference we call the selected interface hacknic
    user_device = clients[int(device_choice)]
    return user_device
