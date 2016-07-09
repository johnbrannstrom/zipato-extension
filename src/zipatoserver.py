#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import requests
import re
import argparse
import traceback
from time import sleep
from flask import Flask
from flask import request
from settings import Settings
from logfile import LogFile
from debug import Debug


class ZipatoServer(Settings, Debug):
    """Zipato extension web server."""

    def _poweron(self):
        """
        Start remote node with a wake on LAN packet.

        :rtype: str
        :returns: Status message

        """
        mac = request.args.get('mac')
        host = request.args.get('host')
        # Check input parameters
        if mac is None:
            return "Error 'poweron' must have parameter 'mac'!"
        # Power on node
        if host is not None:
            command = "{}wakeonlan -i {} {}"
            command = command.format(self.WAKEONLAN_PATH, host, mac)
        else:
            command = "{}wakeonlan {}".format(self.WAKEONLAN_PATH, mac)
        for i in range(3):
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            stdout, stderr = p.communicate()
            sleep(0.1)
        return stdout + stderr

    def _poweroff(self):
        """
        Log on to remote node and shut it down.

        .. note::

            Password less login with SSH keys must be set up for this to work.

        :rtype: str
        :returns: Status message

        """
        user = request.args.get('user')
        host = request.args.get('host')
        if user is None:
            return "Error 'poweroff' must have parameter 'user'!"
        if host is None:
            return "Error 'poweroff' must have parameter 'host'!"
        # Power off node
        command = "{}ssh -i {} -T {}@{} 'shutdown -h now'"
        command = command.format(self.SSH_PATH, self.SSH_KEY_PATH, user, host)
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True)
        stdout, stderr = p.communicate()
        return stdout + stderr

    def _ping(self):
        """
        Ping a node and set Zipato status.

        :rtype: str
        :returns: Status message

        """
        host = request.args.get('host')
        if host is None:
            return "Error 'ping' must have parameter 'host'!"
        for i in range(self.PING_COUNT):
            command = "{}ping -c {} {}".format(self.PING_PATH, str(self.PING_COUNT), host)
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            stdout, stderr = p.communicate()
            result = re.match('.*0 received.*', str(stdout), re.DOTALL)
            ping_ok = result is None
            if ping_ok:
                break
            sleep(5)
        serial = self.ZIPATO_SERIAL
        if host in self.API_PING_HOSTS.keys():
            ep = self.API_PING_HOSTS[host]['ep']
            apikey = self.API_PING_HOSTS[host]['apikey']
            # Set the status of a Zipato sensor to the ping status
            command = ("https://my.zipato.com/zipato-web/remoting/attribute/se"
                       "t?serial={}&ep={}&apikey={}&state={}")
            if ping_ok:
                command = command.format(serial, ep, apikey, 'true')
            else:
                command = command.format(serial, ep, apikey, 'false')
            r = requests.get(command)
            return str(r.status_code)
        else:
            # Just return a the ping status
            if ping_ok:
                return '1'
            else:
                return '0'

    def handle_request(self):
        """Web server function."""
        user = request.args.get('user')
        host = request.args.get('host')
        mac = request.args.get('mac')
        try:
            if request.path == self.WEB_API_PATH + 'poweron':
                message = 'poweron?mac={}&host={}'
                message = message.format(str(mac), str(host))
                result = self._poweron()
            elif request.path == self.WEB_API_PATH + 'poweroff':
                message = 'poweroff?user={}&host={}'
                message = message.format(str(user), str(host))
                result = self._poweroff()
            elif request.path == self.WEB_API_PATH + 'ping':
                message = 'poweroff?host={}'
                message = message.format(str(host))
                result = self._ping()
        except:
            error_log = LogFile(self.ERROR_LOG)
            error_log.write(message)
            error_log.write(traceback.format_exc(), date_time=False)
            error_log.close()
        else:
            message_log = LogFile(self.MESSAGE_LOG)
            message_log.write(message)
            message_log.close()
        return result


class Main(Settings):
    """Contains the script"""

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.

        :rtype: Namespace

        """
        debug_help = 'Debugging on or off.'
        description = 'Start Zipato extension web server.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--debug', type=int,
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args

    def run(self):
        """Run the script"""
        args = self._parse_command_line_options()
        Settings.DEBUG = args.debug
        zipatoserver.run(
            debug=Settings.DEBUG,
            host='0.0.0.0',
            port=self.TCP_PORT,
            processes=self.PROCESSES)


Settings.load_settings_from_yaml()
zipatoserver = Flask(__name__,
                     static_folder='html_static',
                     template_folder='html_templates')

@zipatoserver.route(Settings.WEB_GUI_PATH)
@zipatoserver.route(Settings.WEB_API_PATH + 'poweron')
@zipatoserver.route(Settings.WEB_API_PATH + 'poweroff')
@zipatoserver.route(Settings.WEB_API_PATH + 'ping')

def index():
    """Handle incomming HTTP requests."""
    web_server = ZipatoServer()
    return web_server.handle_request()

if __name__ == '__main__':
    main = Main()
    main.run()
