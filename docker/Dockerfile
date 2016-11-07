# Dockefile for Zipato-extension con
FROM ubuntu:16.04

# Install packages
RUN apt-get update && \
    apt-get -y install python3-pip cron wakeonlan ssh-client iputils-ping \
    --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    mysql-server && \
    pip3 install --upgrade pip && \
    pip3 install setuptools && \
    pip3 install pyyaml flask requests && \
    apt-get remove -y python-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Timezone
RUN  rm /etc/localtime && \
ln -s /usr/share/zoneinfo/Europe/Stockholm /etc/localtime

# Terminal
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Prepare environment for zipato-extension and copy program to image
RUN mkdir -p /mnt/host/var/log && \
mkdir -p /mnt/host/etc
COPY zipato-extension/src /usr/local/bin/zipatoserver
RUN chmod +x /usr/local/bin/zipatoserver/zipatoserver.py && \
chmod +x /usr/local/bin/zipatoserver/ping.py
EXPOSE 80

# TODO test
#RUN mkdir -p /home/john/.ssh
#COPY /home/john/.ssh/id_rsa /home/john/.ssh/id_rsa

# Add programs for autostart
RUN touch "/tmp/start.sh" && \
chmod +x "/tmp/start.sh" && \
echo "cron" >> "/tmp/start.sh" && \
echo "/usr/local/bin/zipatoserver/zipatoserver.py"  >> "/tmp/start.sh"
CMD ["/bin/bash", "/tmp/start.sh"]
