from scapy import Dot11 ,sniff

#To_do lists of mac addresses and other necessary info
ap_list=[]
def PacketHendler(packet):
    if packet.haslayer(Dot11):
        #type -menegment subtype-beacon
        if packet.type==0 and packet.subtype==8:
            #address 2 - transmitter.
            if packet.addr2 not in ap_list:
                ap_list.append(packet.addr2)
                print("Access Point Mac: %s with SSID:%s" %(packet.addr2 ,packet.info))

#insert chosen adapter & packet to PacketHendler
sniff(iface=,pm=PacketHendler)