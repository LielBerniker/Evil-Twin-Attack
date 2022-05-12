#!/bin/sh
# systemd-resolved is a system service that provides network name resolution to local applications
# here we Disable and stop the systemd-resolved service which stop the local DNS stub listener that uses port 53
systemctl stop systemd-resolved>/dev/null 2>&1
systemctl disable systemd-resolved.service >/dev/null 2>&1
systemctl mask systemd-resolved >/dev/null 2>&1
 # set the current interface not to managed mode
nmcli dev set ${INTERFACE} managed no
# change the interface ip and netmask
ifconfig ${INTERFACE} inet 10.0.0.1 netmask 255.255.255.0
# define the default gateway
route add default gw 10.0.0.1

# port 80 is saved for http this is why we do a redirect to port 8080 so we will not need to give a
# root privilege to the users that will use our server
# IP forwarding/Internet routing - is a process used to determine which path a packet or datagram can be sent.
#
echo 1 > /proc/sys/net/ipv4/ip_forward
# in iptables the PREROUTING is : Immediately after being received by an interface.
# go to the nat table ,prerouting ,tcp packets, all packet match the destination of port 80 wil be redirected to port 8080
# and redirect to the destination ip 10.0.0.1
sudo iptables --table nat --append PREROUTING --protocol tcp --dport 80 --jump REDIRECT --to-port 8080
sudo iptables --table nat --append PREROUTING --protocol tcp --dport 80 --jump DNAT --to-destination '
        '10.0.0.1:8080
# in iptables the OUTPUT is: Right after being created by a local process.
# go to the nat table ,output ,tcp packets, all packet match the destination of port 80 wil be redirected to port 8080
# and redirect to the destination ip 10.0.0.1
sudo iptables --table nat --append OUTPUT --protocol tcp --dport 80 --jump REDIRECT --to-port 8080
sudo iptables --table nat --append OUTPUT --protocol tcp --dport 80 --jump DNAT --to-destination 10.0.0.1:8080

#in iptables the POSTROUTING is: Right before leaving an interface in the packet traffic
# here we set it to our interface
sudo iptables --table nat --append POSTROUTING --out-interface ${INTERFACE} --jump MASQUERADE

# Enable forwarding
sudo iptables -P FORWARD ACCEPT

sudo iptables -A INPUT -j ACCEPT >> /dev/null 2>&1
sudo iptables -A OUTPUT -j ACCEPT >> /dev/null 2>&1