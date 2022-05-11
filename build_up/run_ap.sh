
dnsmasq -C build_up/dnsmasq.conf
gnome-terminal -- sh -c "npm --prefix ./captive_portal/ start"
route add default gw 10.0.0.1
hostapd build_up/hostapd.conf -B
route add default gw 10.0.0.1
