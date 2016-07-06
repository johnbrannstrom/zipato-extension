#!/usr/bin/python3

import subprocess
import requests
import re
import argparse
from time import sleep
from flask import Flask
from flask import request
from settings import Settings
from logfile import LogFile


class ZipatoServer:
    """Zipato extension web server."""

    def poweron(self):
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

    def poweroff(self):
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

    def ping(self):
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

    def handle_request(self):
        """Web server function."""
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

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.

        :rtype: Namespace

        """
        debug_help = 'Debugging on or off.'
        description = 'Start Zipato extension web server.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--debug', type=bool,
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args


    def run(self):
        """Run the web server."""
        args = self._parse_command_line_options()
        Settings.DEBUG = args.debug
        zipatoserver.run(
            debug=Settings.DEBUG,
            host='0.0.0.0',
            port=self.TCP_PORT,
            processes=self.PROCESSES)

zipatoserver = Flask(__name__,
                     static_folder='html_static',
                     template_folder='html_templates')
@zipatoserver.route(HTTP_PATH)

def index():
    """Handle incomming HTTP requests."""
    web_server = ZipatoServer()
    return web_server.handle_request()


if __name__ == '__main__':
    web_server = ZipatoServer()
    web_server.run()
