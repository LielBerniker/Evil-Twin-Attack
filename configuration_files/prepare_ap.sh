#!/bin/sh


systemctl disable systemd-resolved.service >/dev/null 2>&1
systemctl stop systemd-resolved>/dev/null 2>&1
systemctl mask systemd-resolved >/dev/null 2>&1
    # Stop system network service
    # os.system('service NetworkManager stop')

sudo ifconfig ${INTERFACE} down
sudo iwconfig ${INTERFACE} mode monitor
sudo ifconfig ${INTERFACE} up

# nmcli dev set ${INTERFACE} managed no
ifconfig ${INTERFACE} 10.0.0.1 netmask 255.255.255.0
route add default gw 10.0.0.1

echo 1 > /proc/sys/net/ipv4/ip_forward
sudo iptables --table nat --append PREROUTING --protocol tcp --dport 80 --jump REDIRECT --to-port 8080
sudo iptables --table nat --append PREROUTING --protocol tcp --dport 80 --jump DNAT --to-destination '
        '10.0.0.1:8080
sudo iptables --table nat --append OUTPUT --protocol tcp --dport 80 --jump REDIRECT --to-port 8080
sudo iptables --table nat --append OUTPUT --protocol tcp --dport 80 --jump DNAT --to-destination 10.0.0.1:8080

sudo iptables --table nat --append POSTROUTING --out-interface ${INTERFACE} --jump MASQUERADE
sudo iptables -P FORWARD ACCEPT
sudo iptables -A INPUT -j ACCEPT >> /dev/null 2>&1
sudo iptables -A OUTPUT -j ACCEPT >> /dev/null 2>&1