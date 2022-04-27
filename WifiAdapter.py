from ctypes import Union
import os
import re # import for regular expressions-Regex.
# We will be using the subprocess module to run commands
import subprocess
import scapy.all as scapy
#from scapy.layers.l2 import ARP, Ether


def MonitorMode(iface):
    os.system("sudo ifconfig " + iface + " down")
    os.system("sudo iwconfig " + iface + " mode monitor")
    os.system("sudo ifconfig " + iface + " up")



def WifiAdapterFinder():
    # Regex to find wireless interfaces.
    # wlan0 = wifi card
    wlan_pattern1 = re.compile("^wlan[0-9]+")
    wlan_pattern2 = re.compile("wlxc83a35c2e0b4")

    # Subprocess is the task of running other programs in Python by creating a new process
    # We run the iwconfig command to look for wireless interfaces.
    # The script is the parent process and creates a child process which runs the system command,
    # and will only continue once the child process has completed.
    # Using the regex.findall () to get a list of matched strings
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
            # checking if the wifi_interface_choice exist in our list
            if check_wifi_result[int(wifi_interface_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")

    # For easy reference we call the selected interface hacknic
    hacknic = check_wifi_result[int(wifi_interface_choice)]
    print (hacknic)
    return hacknic