#!/bin/bash

# Parse command line options
BRANCH="master"
NO_CACHE=""
TAG="zipato-extension"
PORT="80"
DOCKERFILE="Dockerfile_master"
MANUAL_DOCKERFILE="False"
while [[ $# -gt 0 ]]
do
    KEY="$1"
    case ${KEY} in
        -b|--branch)
        BRANCH="$2"
        shift # past argument
        ;;
        -t|--tag)
        TAG="$2"
        shift # past argument
        ;;
        -p|--port)
        PORT="$2"
        shift # past argument
        ;;
        -d|--dockerfile)
        DOCKERFILE="$2"
        MANUAL_DOCKERFILE="True"
        shift # past argument
        ;;
        -n|--no-cache)
        NO_CACHE="--no-cache"
        ;;
        -h|--help)
        echo "Usage: build_zipato_extension_image.sh [-b] [-t] [-n] [-h]"
        echo -e "\nOptional arguments:"
        echo "-b --branch:     Git branch. Default is '${BRANCH}'."
        echo "-t --tag:        Docker image name. Default is 'zipato-extension\
'."
        echo "-n --nocache:    Don't use cache when building image. Default is\
 to use cache."
        echo "-p --port:       Expose port to outside. Default value: 80"
        echo "-d --dockerfile: Specifies what Dockerfile to use. Default is \
'${DOCKERFILE}'".
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

# Select dockerfile
if [ "$BRANCH" != "master" ] && [ "$MANUAL_DOCKERFILE" == "False" ]; then
    DOCKERFILE="Dockerfile_other"
fi

# Build image
git clone https://github.com/johnbrannstrom/zipato-extension -b ${BRANCH} \
    --single-branch zipato-extension
docker build . -t ${TAG} ${NO_CACHE} -f ${DOCKERFILE} \
--build-arg PORT=${PORT} \
--build-arg TAG=${TAG}
rm -Rf zipato-extension
