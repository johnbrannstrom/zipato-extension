#!/bin/bash

# Parse command line options
BRANCH="master"
NO_CACHE=false
TAG="zipato-extension"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -b|--branch)
        BRANCH="$2"
        shift # past argument
        ;;
        -t|--tag)
        TAG="$2"
        shift # past argument
        ;;
        -n|--no-cache)
        NO_CACHE=true
        ;;
        -h|--help)
        echo "Usage: build_zipato_extension_image [-b] [-t] [-n] [-h]"
        echo -e "\nOptional arguments:"
        echo "-b --branch: Git branch. Default value is 'master'."
        echo "-t --tag:    Docker image name. Default value is 'zipato-extension'."
        echo "--nocache:   Don't use cache when building image."
        echo "-h --help:   Display this help."
        exit 0
        ;;
        *)
        # unknown option
        ;;
    esac
    shift # past argument or value
done

# Build image
git clone https://github.com/johnbrannstrom/zipato-extension -b "$BRANCH" \
--single-branch zipato-extension
if [ "$NO_CACHE" = true ]; then
    docker build . -t "$TAG" --no-cache
else
    docker build . -t "$TAG"
fi
rm -Rf zipato-extension
