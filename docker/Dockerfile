# Dockefile for Zipato-extension con
FROM ubuntu:16.04
# Install temporary packages
RUN apt-get update && \
    apt-get -y install python3-pip cron --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    mysql-server && \
    pip3 install --upgrade pip && \
    pip3 install setuptools && \
    pip3 install pyyaml flask && \
    apt-get remove -y python-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# Prepare environment for zipato-extension an copy program to image
RUN mkdir -p /mnt/host/var/log
RUN mkdir -p /mnt/host/etc
COPY zipato-extension/src /usr/local/bin/zipatoserver
RUN chmod +x /usr/local/bin/zipatoserver/zipatoserver.py
RUN chmod +x /usr/local/bin/zipatoserver/ping.py
EXPOSE 80
CMD ["/bin/bash"]
