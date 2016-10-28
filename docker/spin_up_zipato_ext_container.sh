#!/bin/bash -x
docker rm zipato-extension
docker create -ti --name zipato-extension -v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc zipato-extension:latest /bin/bash
docker start zipato-extension
