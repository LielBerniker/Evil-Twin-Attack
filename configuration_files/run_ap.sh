
dnsmasq -C build_up/dnsmasq.conf
gnome-terminal -- sh -c "cd captiv_portal && npm start"
route add default gw 10.0.0.1
hostapd build_up/hostapd.conf -B
route add default gw 10.0.0.1
