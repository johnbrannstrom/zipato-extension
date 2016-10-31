#!/bin/bash
# Parse command line options
NAME="zipato-extension"
IMAGE="zipato-extension"
PORT="80"
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
        echo "spin_up_zipato_ext_container"
        echo "-i --image: Image name to build container from."
        echo "-p --port: Expose this port to ouside of the container."
        echo "-h --help: Display this help."
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
docker create -ti --name "$NAME" -p "$PORT":"$PORT" \
-v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc "$IMAGE":latest /bin/bash
docker start zipato-extension
