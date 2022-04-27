import os
# We require regular expressions.
import re
import csv
# We will be using the subprocess module to run commands on Kali Linux.
import subprocess
import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether

active_wireless_networks = []

def check_for_essid(essid, lst):
    check_status = True

    # If no ESSIDs in list add the row
    if len(lst) == 0:
        return check_status

    # This will only run if there are wireless access points in the list.
    for item in lst:
        # If True don't add to list. False will add it to list
        if essid in item["ESSID"]:
            check_status = False

    return check_status
def find_all_wifi_available():
    # Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
    for file_name in os.listdir():
    # We should only have one csv file as we delete them from the folder every time we run the program.
        if ".csv" in file_name:
            print("There shouldn't be any .csv files in your directory. We found .csv files in your directory.")
            # We get the current working directory.
            directory = os.getcwd()
            try:
                # We make a new directory called /backup
                os.mkdir(directory + "/backup/")
            except:
                print("Backup folder exists.")
            # Create a timestamp
            timestamp = datetime.now()
            # We copy any .csv files in the folder to the backup folder.
            shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
    wlan_pattern = re.compile("wlxc83a35c2e0b4")

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
    print("WiFi adapter connected!\nNow let's kill conflicting processes:")

    # subprocess.run(<list of command line arguments goes here>)
    # The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    # Killing all conflicting processes using airmon-ng
    kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

    # Put wireless in Monitored mode
    print("Putting Wifi adapter into monitored mode:")
    put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

    # subprocess.Popen(<list of command line arguments goes here>)
    # The Popen method opens a pipe from a command. The output is an open file that can be accessed by other programs.
    # We run the iwconfig command to look for wireless interfaces.
    # Discover access points
    discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Loop that shows the wireless access points. We use a try except block and we will quit the loop by pressing ctrl-c.
    try:
        while True:
            # We want to clear the screen before we print the network interfaces.
            subprocess.call("clear", shell=True)
            for file_name in os.listdir():
                    # We should only have one csv file as we backup all previous csv files from the folder every time we run the program. 
                    # The following list contains the field names for the csv entries.
                    fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                    if ".csv" in file_name:
                        with open(file_name) as csv_h:
                            # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above. 
                            # This creates a list of dictionaries with the keys as specified in the fieldnames.
                            csv_h.seek(0)
                            csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                            for row in csv_reader:
                                if row["BSSID"] == "BSSID":
                                    pass
                                elif row["BSSID"] == "Station MAC":
                                    break
                                elif check_for_essid(row["ESSID"], active_wireless_networks):
                                    active_wireless_networks.append(row)

            print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
            print("No |\tBSSID              |\tChannel|\tESSID                         |")
            print("___|\t___________________|\t_______|\t______________________________|")
            for index, item in enumerate(active_wireless_networks):
                # We're using the print statement with an f-string. 
                # F-strings are a more intuitive way to include variables when printing strings, 
                # rather than ugly concatenations.
                print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            # We make the script sleep for 1 second before loading the updated list.
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReady to make choice.")

    # Ensure that the input choice is valid.
    while True:
        choice = input("Please select a choice from above: ")
        try:
            if active_wireless_networks[int(choice)]:
                break
        except:
            print("Please try again.")


if __name__ == '__main__':

    # wifi_info = find_all_wifi_available()
    # user_device_info = find_all_users_in_network(wifi_info)
      
    request = scapy.ARP() 
        
    request.pdst = '192.168.0.1/24'
    broadcast = scapy.Ether() 
        
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'
        
    request_broadcast = broadcast / request 
    clients = scapy.srp(request_broadcast, timeout = 10,verbose = 1)[0] 
    for element in clients: 
        print(element[1].psrc + "      " + element[1].hwsrc) 

















# from json.tool import main
# import os
# # We require regular expressions.
# import re
# import csv
# # We will be using the subprocess module to run commands on Kali Linux.
# import subprocess
# from scapy.all import *
# from scapy.layers.l2 import ARP, Ether
# import WifiAdapter as WAF
# import sys

# # # IFACE = WAF.WifiAdapterFinder()
# # # IFACE_NAME = WAF.MonitorMode(IFACE)
# # iface = "wlan0mon"
# # devices = set()


# # def PacketHandler(pkt):
# #     print("packet found")
# #     if pkt.haslayer(Dot11):
# #         dot11_layer = pkt.getlayer(Dot11)
# #         print("packet has layer dot11")  
# #         if dot11_layer.addr2 and (dot11_layer.addr2 not in devices):
# #             devices.add(dot11_layer.addr2)
# #             print((len(devices) -1 ), dot11_layer.addr2, dot11_layer.payload.name)
  
  
# # sniff(iface=iface,prn=PacketHandler)






# active_wireless_networks = []

# def check_for_essid(essid, lst):
#     check_status = True

#     # If no ESSIDs in list add the row
#     if len(lst) == 0:
#         return check_status

#     # This will only run if there are wireless access points in the list.
#     for item in lst:
#         # If True don't add to list. False will add it to list
#         if essid in item["ESSID"]:
#             check_status = False

#     return check_status
# def find_all_wifi_available():
#     # Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
#     for file_name in os.listdir():
#     # We should only have one csv file as we delete them from the folder every time we run the program.
#         if ".csv" in file_name:
#             print("There shouldn't be any .csv files in your directory. We found .csv files in your directory.")
#             # We get the current working directory.
#             directory = os.getcwd()
#             try:
#                 # We make a new directory called /backup
#                 os.mkdir(directory + "/backup/")
#             except:
#                 print("Backup folder exists.")
#             # Create a timestamp
#             timestamp = datetime.now()
#             # We copy any .csv files in the folder to the backup folder.
#             shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
#     wlan_pattern = re.compile("wlxc83a35c2e0b4")

#     # Python allows is to run system commands by using a function provided by the subprocess module.
#     # subprocess.run(<list of command line arguments goes here>)
#     # The script is the parent process and creates a child process which runs the system command,
#     # and will only continue once the child process has completed.
#     # We run the iwconfig command to look for wireless interfaces.
#     check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

#     # No WiFi Adapter connected.
#     if len(check_wifi_result) == 0:
#         print("Please connect a WiFi adapter and try again.")
#         exit()

#     # Menu to select WiFi interface from
#     print("The following WiFi interfaces are available:")
#     for index, item in enumerate(check_wifi_result):
#         print(f"{index} - {item}")
#     # Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
#     while True:
#         wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
#         try:
#             if check_wifi_result[int(wifi_interface_choice)]:
#                 break
#         except:
#             print("Please enter a number that corresponds with the choices available.")

#     # For easy reference we call the selected interface hacknic
#     hacknic = check_wifi_result[int(wifi_interface_choice)]
#     print("WiFi adapter connected!\nNow let's kill conflicting processes:")

#     # subprocess.run(<list of command line arguments goes here>)
#     # The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
#     # We run the iwconfig command to look for wireless interfaces.
#     # Killing all conflicting processes using airmon-ng
#     kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

#     # Put wireless in Monitored mode
#     print("Putting Wifi adapter into monitored mode:")
#     put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

#     # subprocess.Popen(<list of command line arguments goes here>)
#     # The Popen method opens a pipe from a command. The output is an open file that can be accessed by other programs.
#     # We run the iwconfig command to look for wireless interfaces.
#     # Discover access points
#     discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#     # Loop that shows the wireless access points. We use a try except block and we will quit the loop by pressing ctrl-c.
#     try:
#         while True:
#             # We want to clear the screen before we print the network interfaces.
#             # subprocess.call("clear", shell=True)
#             for file_name in os.listdir():
#                     # We should only have one csv file as we backup all previous csv files from the folder every time we run the program. 
#                     # The following list contains the field names for the csv entries.
#                     fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
#                     if ".csv" in file_name:
#                         with open(file_name) as csv_h:
#                             # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above. 
#                             # This creates a list of dictionaries with the keys as specified in the fieldnames.
#                             csv_h.seek(0)
#                             csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
#                             for row in csv_reader:
#                                 if row["BSSID"] == "BSSID":
#                                     pass
#                                 elif row["BSSID"] == "Station MAC":
#                                     break
#                                 elif check_for_essid(row["ESSID"], active_wireless_networks):
#                                     active_wireless_networks.append(row)

#             print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
#             print("No |\tBSSID              |\tChannel|\tESSID                         |")
#             print("___|\t___________________|\t_______|\t______________________________|")
#             for index, item in enumerate(active_wireless_networks):
#                 # We're using the print statement with an f-string. 
#                 # F-strings are a more intuitive way to include variables when printing strings, 
#                 # rather than ugly concatenations.
#                 print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
#             # We make the script sleep for 1 second before loading the updated list.
#             time.sleep(1)

#     except KeyboardInterrupt:
#         print("\nReady to make choice.")

#     # Ensure that the input choice is valid.
#     while True:
#         choice = input("Please select a choice from above: ")
#         try:
#             if active_wireless_networks[int(choice)]:
#                 break
#         except:
#             print("Please try again.")



# def find_all_users_in_network(target_ip):
#     # create ARP packet
#     arp = ARP(pdst=target_ip)
#     # create the Ether broadcast packet
#     # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
#     ether = Ether(dst="ff:ff:ff:ff:ff:ff")
#     # stack them
#     packet = ether / arp
#     result = srp(packet, timeout=3, verbose=0)[0]
#     # a list of clients, we will fill this in the upcoming loop
#     clients = []
#     for sent, received in result:
#         # for each response, append ip and mac address to `clients` list
#         clients.append({'ip': received.psrc, 'mac': received.hwsrc})
#     # print clients
#     print("Available devices in the network:")
#     print("IP" + " " * 18 + "MAC")
#     for index, client in clients:
#         print(f"{index}" + "{:16}    {}".format(client['ip'], client['mac']))
#     while True:
#         device_choice = input("Please select the device you want to use for the attack: ")
#         try:
#             if clients[int(device_choice)]:
#                 break
#         except:
#             print("Please enter a number that corresponds with the choices available.")

#         # For easy reference we call the selected interface hacknic
#     user_device = clients[int(device_choice)]
#     return user_device

# if __name__ == "__main__":
#     find_all_wifi_available()


    