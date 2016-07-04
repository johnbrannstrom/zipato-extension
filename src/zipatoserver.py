#!/usr/bin/python3

import subprocess
import requests
import re
import datetime
from time import sleep
from flask import Flask
from flask import request

# The service will respond to requests on this port
TCP_PORT = 5000

# The service will respons to requests on this HTTP path
HTTP_PATH = '/'

# Sets if debug mode should be used
debug = False

# Set if logging should be used
LOGGING = True

# Full path and name of log file
LOG_FILE_NAME = '/home/john/httpaction'

# Path to the wakeonlan command
WAKEONLAN_PATH = '/usr/bin/'

# Path to the ping command
PING_PATH = '/bin/'

# Number of pings
PING_COUNT = 3

# Path to the ssh command
SSH_PATH = '/usr/bin/'

# Path to ssh key directory
SSH_KEY_PATH = '/home/john/.ssh/id_rsa'

zipatoserver = Flask(__name__)


class LogFile:
    """Log file container."""

    def __init__(self, name):
        """Initializes a LogFile instance."""
        self.file = open(name, 'a+')

    def write(self, message):
        """
        Write line to log file.

        :param str message: Log message.

        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = now + ' ' + message + '\n'
        self.file.write(line)

    def close(self):
        """Close log file."""
        self.file.close()


@zipatoserver.route(HTTP_PATH)
def index():
    """Web server function."""

    def poweron():
        """
        Start remote node with a wake on LAN packet.

        :rtype: str
        :returns: Status message

        """
        if mac is not None:
            if host is not None:
                command = "{}wakeonlan -i {} {}"
                command = command.format(WAKEONLAN_PATH, host, mac)
            else:
                command = "{}wakeonlan {}".format(WAKEONLAN_PATH, mac)
            for i in range(3):
                p = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True)
                stdout, stderr = p.communicate()
                sleep(0.1)
            if LOGGING:
                log_file.write(command)
            return stdout + stderr
        else:
            return "Action 'poweron' must have parameter 'mac'!"

    def poweroff():
        """
        Log on to remote node and shut it down.

        .. note::

            Password less login with SSH keys must be set up for this to work.

        :rtype: str
        :returns: Status message

        """
        if user is not None and host is not None:
            command = "{}ssh -i {} -T {}@{} 'shutdown -h now'"
            command = command.format(SSH_PATH, SSH_KEY_PATH, user, host)
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            stdout, stderr = p.communicate()
            if LOGGING:
                log_file.write(command)
            return stdout + stderr
        elif user is None:
            return "Action 'poweroff' must have parameter 'user'!"
        elif host is None:
            return "Action 'poweroff' must have parameter 'host'!"

    def ping():
        """
        Ping an IP address return the status.

        :rtype: str
        :returns: Status message

        """
        if host is not None:
            for i in range(PING_COUNT):
                command = "{}ping -c {} {}".format(PING_PATH, str(PING_COUNT), host)
                p = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True)
                stdout, stderr = p.communicate()
                if LOGGING:
                    log_file.write(command)
                result = re.match('.*0 received.*', str(stdout), re.DOTALL)
                ping_ok = result is None
                if ping_ok:
                    break
                sleep(5)
            if serial is not None and ep is not None and apikey is not None:
                # Set the status of a Zipato sensor to the ping status
                command = "https://my.zipato.com/zipato-web/remoting/attribute/set?serial={}&ep={}&apikey={}&state={}"
                if ping_ok:
                    command = command.format(serial, ep, apikey, 'true')
                else:
                    command = command.format(serial, ep, apikey, 'false')
                r = requests.get(command)
                if LOGGING:
                    log_file.write(command)
                return str(r.status_code)
            else:
                # Just return a the ping status
                if ping_ok:
                    return '1'
                else:
                    return '0'
        else:
            return "Action 'ping' must have parameter 'host'!"

    action = request.args.get('action')
    mac = request.args.get('mac')
    user = request.args.get('user')
    host = request.args.get('host')
    serial = request.args.get('serial')
    ep = request.args.get('ep')
    apikey = request.args.get('apikey')
    if LOGGING:
        log_file = LogFile(LOG_FILE_NAME)
    if action.lower() == 'poweron':
        result = poweron()
    elif action.lower() == 'poweroff':
        result = poweroff()
    elif action.lower() == 'ping':
        result = ping()
    else:
        result = ("Unknown value '{}' for paramater 'action'. Choose from 'pow"
                  "eron, poweroff, ping'!")
        result = result.format(action)
    if LOGGING:
        log_file.close()
    return result


if __name__ == '__main__':
    zipatoserver.run(debug=debug, host='0.0.0.0', port=TCP_PORT, threaded=True)
