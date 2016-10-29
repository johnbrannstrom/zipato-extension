#!/bin/bash -x
# Parse command line options
NAME="zipato-extension"
IMAGE="zipato-extension"
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
        *)
        # unknown option
        ;;
    esac
    shift # past argument or value
done

# Delete old container
docker rm "$NAME"
# Create new container
docker create -ti --name "$NAME" -p 80:80 \
-v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc "$IMAGE":latest /bin/bash
docker start zipato-extension
