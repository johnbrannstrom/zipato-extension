Features
--------
* Adds the ability to ping IP network devices and then set the status of a virtual Zipato sensor.
* Adds the ability to start IP network devices with wake-on-lan.
* Adds the ability to shut down Linux hosts by logging on to them and issuing the *shutdown -r now* command.

Environment requirements
------------------------

* Tested on docker 1.12.2 on Linux

Installation instructions
------------------------

* Pull the image from docker with the following command
  ```
  docker pull johnbrannstrom/zipato-extension && docker tag johnbrannstrom/zipato-extension:latest zipato-extension:latest
  ```

* Start a container with the image by running the script. [spin_up_zipato_ext_container.sh](https://raw.githubusercontent.com/johnbrannstrom/zipato-extension/master/docker/spin_up_zipato_ext_container.sh)
