#!/bin/bash
# Parse command line options
NAME="zipato-extension"
IMAGE="zipato-extension"
PORT="80:80"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        --name)
        NAME="$2"
        shift # past argument
        ;;
        -i|--image)
        IMAGE="$2"
        shift # past argument
        ;;
        -p|--port)
        PORT="$2"
        shift # past argument
        ;;
        -h|--help)
        echo "Usage: spin_up_zipato_ext_container.sh [-i] [-p] [-h]"
        echo -e "\nOptional arguments:"
        echo "-i --image: Image name to build container from."
        echo "            Default value: zipato-extension."
        echo "-p --port:  Expose inside port to outside. Format is outside:inside"
        echo "            Default value: 80:80"
        echo "-h --help:  Display this help."
        exit 0
        ;;
        *)
        # unknown option
        ;;
    esac
    shift # past argument or value
done

# Delete old container
docker stop "$NAME"
docker rm "$NAME"
# Create new container
docker create -ti --name "$NAME" -p "$PORT" \
-v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc "$IMAGE":latest /bin/bash
docker start zipato-extension
