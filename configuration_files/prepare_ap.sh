
#!/bin/sh


systemctl disable systemd-resolved.service
systemctl stop systemd-resolved
service Network-Manager stop
airmon-ng check kill

ifconfig ${INTERFACE} 10.0.0.1 netmask 255.255.255.0

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT

route add default gw 10.0.0.1


echo start
dnsmasq -C build_up/dnsmasq.conf
hostapd build_up/hostapd.conf -B
echo end
service apache2 start
route add default gw 10.0.0.1
echo start please