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
        --no-cache)
        NO_CACHE=true
        ;;
        -h|--help)
        echo "build_zipato_extension_image"
        echo "-b --branch: Git branch."
        echo "-t --tag: Docker image name."
        echo "--nocache: Don't use cache when building image."
        echo "-h --help: Display this help."
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
