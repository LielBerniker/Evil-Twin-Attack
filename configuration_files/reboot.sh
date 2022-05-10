#!/bin/sh
service NetworkManager start
service NetworkManager start
service hostapd stop
service apache2 stop
service dnsmasq stop
service rpcbind stop
killall dnsmasq
killall hostapd
rm -f build_up/hostapd.conf
rm -f build_up/dnsmasq.conf
systemctl enable systemd-resolved.service
systemctl start systemd-resolved
rm -rf build_up/
ifconfig ${INTERFACE} down
iwconfig ${INTERFACE} mode managed
ifconfig ${INTERFACE} up
service network-manager restart