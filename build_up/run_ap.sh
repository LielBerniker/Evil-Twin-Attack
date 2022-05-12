#!/bin/bash
# create the dnamasq by the configuration file settings
dnsmasq -C build_up/dnsmasq.conf
# run the server from an inner dir
gnome-terminal -- sh -c "cd captiv_portal && npm start"
# add default gateway
route add default gw 10.0.0.1
# create the acces point by the settings from the configuration file
hostapd build_up/hostapd.conf -B
route add default gw 10.0.0.1

