#!/bin/bash
# Parse command line options
NAME=""
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
        echo "-i --image: Image name to build container from."
        echo "            Default value: zipato-extension."
        echo "-n --name:  Container name. Default value is same as image name."
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
if [ "${NAME}" == "" ]; then
    NAME="${IMAGE}"
fi

# Delete old container
docker stop "$NAME"
docker rm "$NAME"
# Create the create new container command
COMMAND="docker create -ti --name ${NAME} -p ${PORT}:${PORT} --net=host \
-p 23:23 \
-v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc"
# Add the image to the command
COMMAND="${COMMAND} ${IMAGE}:latest"
echo "${COMMAND}"
# Execute command
eval $COMMAND
# Start the container
docker start ${NAME}
