#!/bin/sh
docker rm zipato-extension
docker create -ti --name zipato-extension -v /var/log:/mnt/host/var/log \
-v /etc:/mnt/host/etc ubuntu:16.04 /bin/bash
docker start zipato-extension