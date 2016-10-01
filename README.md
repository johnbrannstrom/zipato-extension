Features
--------
* Adds the ability to ping IP network devices and then set the status of a virtual Zipato sensor.
* Adds the ability to start IP network devices with wake-on-lan.
* Adds the ability to shut down Linux hosts by logging on to them and issuing the *shutdown -r now* command.

Environment requirements
------------------------

* Tested with *Python 3.4*.
* Tested with the *Google Chrome* browser.
* Python module requirements are listed on the *requirements.txt* file found in the *other* folder.
* Tested with *Ubuntu Linux 14.04.3 LTS*.

Installation instructions
--------------------------

1. Create the */usr/local/bin/zipatoserver* directory on the Linux server where you want to run zipato-extension.
2. Copy all files from the *src* folder in the master branch to the */usr/local/bin/zipatoserver* directory.
3. Copy the *zipatoserver_template.conf* file from the *other* folder in the master branch to */etc/zipatoserver.conf*.
4. Make the *zipatoserver.py* application executable by running the following command *chmod +x /usr/local/bin/zipatoserver.py*.
5. Start the *zipatoserver.py* application by running the following command */usr/local/bin/zipatoserver.py*.
6. Instructions of usage can be found by opening your favourite browser and navigating to the *zipatoserver* application as shown in the following example:
http://ip.address.or.hostname.of.your.server:8080
