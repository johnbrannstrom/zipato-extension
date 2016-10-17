#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Ping
****

This module will ping one host for status and forward that status to a
Zipato sensor.

"""

import subprocess
import argparse
import re
import traceback
from settings import Settings
from zipatoconnection import ZipatoConnection
from time import sleep
from logfile import LogFile


# noinspection PyUnresolvedReferences
class Main(Settings):
    """Contains the script."""

    # noinspection PyUnboundLocalVariable
    def _ping(self, host):
        """
        Ping one host and set status to a Zipato sensor.

        :param str host: Target host.
        :rtype: str
        :returns: Status message

        """
        message_log = LogFile(self.MESSAGE_LOG)
        if host in self.PING_HOSTS.keys():
            ep = self.PING_HOSTS[host]['ep']
            apikey = self.PING_HOSTS[host]['apikey']
        else:
            message = (
                "ping: host={}, Host has not been configured for ping")
            message = message.format(host)
            message_log.write([message])
            return None
        try:
            for i in range(self.PING_COUNT):
                command = "{}ping -c {} {}"
                command = command.format(
                    self.PING_PATH, str(self.PING_COUNT), host)
                p = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True)
                stdout, stderr = p.communicate()
                result = re.match('.*0 received.*', str(stdout), re.DOTALL)
                status = result is None
                if status:
                    break
                sleep(self.PING_INTERVAL)
            # Set the status of a Zipato sensor to the ping status
            zipato_connection = ZipatoConnection(self.ZIPATO_SERIAL)
            if status:
                zipato_connection.set_sensor_status(
                    ep=ep, apikey=apikey, status=True)
            else:
                zipato_connection.set_sensor_status(
                    ep=ep, apikey=apikey, status=False)
        except:
            error_log = LogFile(self.ERROR_LOG)
            message = 'ping: host={}'.format(host)
            error_log.write([message])
            traceback_message = traceback.format_exc()
            error_log.write([traceback_message], date_time=False)
        message = "ping: host={}, status={}".format(host, status)
        message_log.write([message])

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.
        
        :rtype: Namespace
        
        """
        debug_help = 'Debugging printout level.'
        host_help = 'Host or IP address to get ping status for.'
        description = 'Ping one host and set status to a Zipato sensor.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '-o', '--host', type=str, help=host_help, required=True)
        parser.add_argument('--debug', type=int, default=0,
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args
      
    def run(self):
        """
        Run the script.
        
        """
        args = self._parse_command_line_options()
        Settings.load_settings_from_yaml(settings_path='/etc/')
        Settings.DEBUG = args.debug
        self._ping(args.host)

if __name__ == '__main__':
    main = Main()
    main.run()
