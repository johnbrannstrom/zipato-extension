# Buildfile for Ziato-extension docker container
# Build with command:
# docker build . --no-cache
FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python3-pip mysql-server
RUN pip3 install --upgrade pip
RUN pip3 install pyyaml flask
RUN apt install