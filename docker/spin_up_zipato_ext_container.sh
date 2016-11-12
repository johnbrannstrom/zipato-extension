#!/bin/bash
# Parse command line options
NAME="zipato-extension"
IMAGE="zipato-extension"
PORT="80"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -n|--name)
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
        echo "-n --name:  Container name."
        echo "            Default value: zipato-extension."
        echo "-i --image: Image name to build container from."
        echo "            Default value: zipato-extension."
        echo "-p --port:  Expose port to outside. Default value: 80"
        echo "-h --help:  Display this help."
        echo ""
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
docker create -ti --name ${NAME} -p ${PORT}:${PORT} --net=host \
-v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc ${IMAGE}:latest
docker start ${IMAGE}
