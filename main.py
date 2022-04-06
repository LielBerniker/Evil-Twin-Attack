import os
# We require regular expressions.
import re
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
from scapy.all import ARP, Ether, srp

def find_all_wifi_available():
    # Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
    wlan_pattern = re.compile("^wlan[0-9]+")

    # Python allows is to run system commands by using a function provided by the subprocess module.
    # subprocess.run(<list of command line arguments goes here>)
    # The script is the parent process and creates a child process which runs the system command,
    # and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

    # No WiFi Adapter connected.
    if len(check_wifi_result) == 0:
        print("Please connect a WiFi adapter and try again.")
        exit()

    # Menu to select WiFi interface from
    print("The following WiFi interfaces are available:")
    for index, item in enumerate(check_wifi_result):
        print(f"{index} - {item}")
    # Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
    while True:
        wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
        try:
            if check_wifi_result[int(wifi_interface_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")

    # For easy reference we call the selected interface hacknic
    hacknic = check_wifi_result[int(wifi_interface_choice)]
    return hacknic

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
    for index,client in clients:
        print(f"{index}"+"{:16}    {}".format(client['ip'], client['mac']))
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


if __name__ == '__main__':
    wifi_info = find_all_wifi_available()



