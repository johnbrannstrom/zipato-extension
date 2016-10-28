#!/bin/bash -x

# Get command line options
BRANCH="master"
NO_CACHE=false
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -b|--branch)
        BRANCH="$2"
        shift # past argument
        ;;
        --no-cache)
        NO_CACHE=true
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
    docker build . -t zipato-extension --no-cache
else
    docker build . -t zipato-extension
fi
rm -Rf zipato-extension
