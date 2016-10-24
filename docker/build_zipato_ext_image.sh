#!/bin/sh
RUN git clone https://github.com/johnbrannstrom/zipato-extension -b master \
--single-branch /tmp/zipato-extension
docker build . --no-cache -t zipato-extension
RUN rm -Rf /tmp/zipato-extension