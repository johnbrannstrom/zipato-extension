#!/bin/sh -x
git clone https://github.com/johnbrannstrom/zipato-extension -b master \
--single-branch zipato-extension
docker build . --no-cache -t zipato-extension
rm -Rf zipato-extension
