import os
# We require regular expressions.
import re
import csv
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
# import scapy.all as scapy
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



# #!/usr/bin/env python
# # The previous line ensures that this script is run under the context
# # of the Python interpreter. Next, import the Scapy functions:
# from scapy.all import *
# # Define the interface name that we will be sniffing from, you can
# # change this if needed.
# interface = "wlxc83a35c2e0b4"
# # Next, declare a Python list to keep track of client MAC addresses
# # that we have already seen so we only print the address once per client.
# observedclients = []
# # The sniffmgmt() function is called each time Scapy receives a packet
# # (we'll tell Scapy to use this function below with the sniff() function).
# # The packet that was sniffed is passed as the function argument, "p".
# def sniffmgmt(p):
#     # Define our tuple (an immutable list) of the 3 management frame
#     # subtypes sent exclusively by clients. I got this list from Wireshark.
#     stamgmtstypes = (0, 2, 4)
#     # Make sure the packet has the Scapy Dot11 layer present
#     if p.haslayer(Dot11):
#         # Check to make sure this is a management frame (type=0) and that
#         # the subtype is one of our management frame subtypes indicating a
#         # a wireless client
#         if p.type == 0 and p.subtype in stamgmtstypes:
#             # We only want to print the MAC address of the client if it
#             # hasn't already been observed. Check our list and if the
#             # client address isn't present, print the address and then add
#             # it to our list.
#             if p.addr2 not in observedclients:
#                 print (p.show)
#                 observedclients.append(p.addr2)
# # With the sniffmgmt() function complete, we can invoke the Scapy sniff()
# # function, pointing to the monitor mode interface, and telling Scapy to call
# # the sniffmgmt() function for each packet received. Easy!
# sniff(iface=interface, prn=sniffmgmt)