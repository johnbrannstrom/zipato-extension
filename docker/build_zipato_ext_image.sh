#!/bin/bash

# Parse command line options
BRANCH="master"
NO_CACHE=""
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
        NO_CACHE="--no-cache"
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
docker build . -t ${TAG} ${NO_CACHE}
fi
rm -Rf zipato-extension
