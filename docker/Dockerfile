# Buildfile for Ziato-extension docker container
FROM ubuntu:16.04
# Install required packages
RUN apt-get update
RUN apt-get -y install python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server
RUN pip3 install --upgrade pip
RUN pip3 install pyyaml flask
# Prepare environment for zipato-extension an copy program to container
RUN mkdir -p /mnt/host/var/log
RUN mkdir -p /mnt/host/etc
COPY zipato-extension/src /usr/local/bin/zipatoserver
RUN chmod +x /usr/local/bin/zipatoserver/zipatoserver.py
RUN chmod +x /usr/local/bin/zipatoserver/ping.py
