#!/bin/sh
 # Stop and kill the hostapd and dnsmasq services.
 # delete previous files and dir if exist
rm -f build_up/hostapd.conf
rm -f build_up/dnsmasq.conf
rm -rf ../build_up/

# stop hostapd and dnsmasq
service hostapd stop
service dnsmasq stop
killall dnsmasq >/dev/null 2>&1
killall hostapd >/dev/null 2>&1

# systemd-resolved is a system service that provides network name resolution to local applications
# here we enable and start the systemd-resolved service which start the local DNS stub listener that uses port 53
systemctl unmask systemd-resolved >/dev/null 2>&1
systemctl enable systemd-resolved.service >/dev/null 2>&1
systemctl start systemd-resolved >/dev/null 2>&1

 # drop all iptables rules
sudo iptables -F
sudo iptables -X
sudo iptables --table nat -F
sudo iptables --table nat -X
sudo iptables -P OUTPUT ACCEPT
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT


