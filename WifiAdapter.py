from ctypes import Union
import os
# We require regular expressions.
import re
import csv
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether


def MonitorMode(iface):
    os.system("sudo airmon-ng check kill")
    os.system("sudo airmon-ng start "+ iface)
    os.system("clear")
    iface = str(iface)+'mon'
    return iface


def WifiAdapterFinder():
    # Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
    wlan_pattern1 = re.compile("^wlan[0-9]+")
    wlan_pattern2 = re.compile("wlxc83a35c2e0b4")

    # Python allows is to run system commands by using a function provided by the subprocess module.
    # subprocess.run(<list of command line arguments goes here>)
    # The script is the parent process and creates a child process which runs the system command,
    # and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    check_wifi_result1 = wlan_pattern1.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
    check_wifi_result2 = wlan_pattern2.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
    check_wifi_result = check_wifi_result1+check_wifi_result2

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
    print (hacknic)
    return hacknic