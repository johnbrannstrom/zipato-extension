# Buildfile for Ziato-extension docker container
# Build with command:
# docker build . --no-cache -t zipato-extension
FROM ubuntu:16.04
#RUN apt-get update
#RUN apt-get -y install python3-pip
#RUN apt-get -y install mysql-server
#RUN apt-get -y install git
#RUN pip3 install --upgrade pip
#RUN pip3 install pyyaml flask
RUN mkdir -p /mnt/host/var/log
RUN mkdir -p /mnt/host/etc
RUN cd /tmp
RUN git clone https://github.com/johnbrannstrom/zipato-extension
RUN rm -Rf /tmp/zipato-extension