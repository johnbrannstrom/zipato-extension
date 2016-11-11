#!/bin/bash

SUBNET="192.168.0.0/24"
GATEWAY="192.168.0.1"
INTERFACE="eth0"
ADDRESS="192.168.0.83"
NETMASK="255.255.255.0"
BROADCAST="192.168.0.255"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -s|--subnet)
        SUBNET="$2"
        shift # past argument
        ;;
        -g|--gateway)
        GATEWAY="$2"
        shift # past argument
        ;;
        -i|--interface)
        INTERFACE="$2"
        shift # past argument
        ;;
        -n|--netmask)
        NETMASK="$2"
        shift # past argument
        ;;
        -b|--broadcast)
        BROADCAST="$2"
        shift # past argument
        ;;
        -a|--address)
        ADDRESS="$2"
        shift # past argument
        ;;
        -h|--help)
        echo "Usage: create_zipato_ext_net.sh -i -s -g -n -a -b [-h]"
        echo -e "\nOptional arguments:"
        echo "-s --subnet:     Parent interface subnet."
        echo "                 Default value: '${SUBNET}'."
        echo "-n --netmask:    Parent interface netmask."
        echo "                 Default value: '${NETMASK}'."
        echo "-a --address:    IP address on the parent interface subnet, for"
        echo "                 the new zipato-extension interface."
        echo "                 Default value: '${ADDRESS}'."
        echo "-g --gateway:    Parent interface default gateway."
        echo "                 Default value: '${GATEWAY}'."
        echo "-b --broadcast:  Parent interface broadcast address."
        echo "                 Default value: '${BROADCAST}'."
        echo "-i --interface:  Parent interface name."
        echo "                 Default value: '${INTERFACE}'"
        echo "-h --help:       Display this help."
        echo ""
        exit 0
        ;;
        *)
        # unknown option
        ;;
    esac
    shift # past argument or value
done

# Create virtual interface
echo "iface ${INTERFACE}:839 inet static
address ${ADDRESS}
netmask ${NETMASK}
broadcast ${BROADCAST}" >> /etc/network/interfaces
# service networking restart TODO uncomment

# Create docker network
docker network create -d macvlan --subnet=${SUBNET} \
--gateway=${GATEWAY}  -o macvlan_mode=passthru -o parent=${INTERFACE}.839 \
zipato_ext_net
