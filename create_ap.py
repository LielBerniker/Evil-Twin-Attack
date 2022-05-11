import os

from string import Template


def change_template(path, interface, ssid_name):
    with open(path, 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(INTERFACE=interface, SSID_NAME=ssid_name))
        f.truncate()


def interface_change_mode(interface):
    # Start system network service
    # os.system('service NetworkManager start')
    os.system('nmcli dev set ' + interface + ' managed yes')


def prepare_fake_access_point(interface, ssid_name):
    """
    prepare the environment setup for creating the fake access point
    :param access_point_bssid represent the network name
    """
    # os.system('sudo sh configuration_files/reboot.sh')
    # os.system('rm -rf build_up/')
    # os.system('cp -r configuration_files build_up')
    # change_template('build_up/hostapd.conf', interface, ssid_name)
    # change_template('build_up/dnsmasq.conf', interface, ssid_name)
    # change_template('build_up/prepare_ap.sh', interface, ssid_name)
    # os.system('sudo sh build_up/prepare_ap.sh')
    # print("finish prepare conf files")
    # print("run fake ap")
    # os.system('sudo sh build_up/run_ap.sh')


    # interface_change_mode(interface)

    os.system('sudo sh configuration_files/reboot.sh')
