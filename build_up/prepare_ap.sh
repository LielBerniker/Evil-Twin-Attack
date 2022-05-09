
#!/bin/sh


systemctl disable systemd-resolved.service
systemctl stop systemd-resolved
service NetworkManager stop
airmon-ng check kill

ifconfig ${INTERFACE} 10.0.0.1 netmask 255.255.255.0



echo start
dnsmasq -C build_up/dnsmasq.conf
hostapd build_up/hostapd.conf -B
echo end
echo start please