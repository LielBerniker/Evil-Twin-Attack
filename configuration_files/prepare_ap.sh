
#!/bin/sh


systemctl disable systemd-resolved.service >/dev/null 2>&1
systemctl stop systemd-resolved>/dev/null 2>&1
service NetworkManager stop
pkill -9 hostapd
pkill -9 dnsmasq
pkill -9 wpa_supplicant
pkill -9 dhclient
killall dnsmasq >/dev/null 2>&1
killall hostapd >/dev/null 2>&1

ifconfig ${INTERFACE} 10.0.0.1 netmask 255.255.255.0
route add default gw 10.0.0.1

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT


echo start
dnsmasq -C build_up/dnsmasq.conf
gnome-terminal -- sh -c "npm --prefix ./captive_portal/ start"
route add default gw 10.0.0.1
hostapd build_up/hostapd.conf -B
route add default gw 10.0.0.1
echo end
service apache2 start
echo start please