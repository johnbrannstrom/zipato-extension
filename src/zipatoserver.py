#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import pprint
import argparse
import traceback
import json
import codecs
from copy import copy
from time import sleep
from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from settings import Settings
from logfile import LogFile
from debug import Debug
from error import ZipatoError


# noinspection PyUnresolvedReferences
class ZipatoRequestHandler(Settings):
    """Zipato extension web server."""

    @staticmethod
    def _json_response(message, status_code=200):
        """
        Create a json HTTP response.

        :param str message: Text message.
        :param int status_code: HTTP status code
        :rtype: Json
        :return: Json HTTP response

        """
        data = {
            'status': status_code,
            'message': message
        }
        json_message = json.dumps(data)
        return Response(
            json_message, status=status_code, mimetype='application/json')

    # noinspection PyGlobalUndefined,PyUnboundLocalVariable
    def _poweron(self):
        """
        Start remote node with a wake on LAN packet.

        :rtype: str
        :returns: Status message

        """
        global stdout
        mac = request.args.get('mac')
        host = request.args.get('host')
        # Check input parameters
        if mac is None:
            message = "Error 'poweron' must have parameter 'mac'!"
            return self._json_response(message, 400)
        # Power on node
        if host is not None:
            command = "{}etherwake -i {} {}"
            command = command.format(self.WAKEONLAN_PATH, host, mac)
        else:
            command = "{}etherwake {}".format(self.WAKEONLAN_PATH, mac)
        for i in range(3):
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            stdout, stderr = p.communicate()
            sleep(0.1)
        message = codecs.decode(stdout + stderr, 'utf-8')
        return self._json_response(message, 200)

    # noinspection PyShadowingNames
    def _poweroff(self):
        """
        Log on to remote node and shut it down.

        :rtype: str
        :returns: Status message

        """
        host = request.args.get('host')
        if host is None:
            message = "Error 'poweroff' must have parameter 'host'!"
            return self._json_response(message, 400)
        if host in self.API_POWEROFF_HOSTS.keys():
            user = self.API_POWEROFF_HOSTS[host]['user']
        else:
            message = "Error host '{}' has not been configured for 'poweroff'!"
            message = message.format(host)
            return self._json_response(message, 400)
        # Power off node
        command = ("{}ssh -o 'StrictHostKeyChecking no' -i {} -T {}@{} 'shutdo"
                   "wn -h now'")
        ssh_key_file = self.SSH_KEY_FILE.replace('$HOST', host)
        command = command.format(self.SSH_PATH, ssh_key_file, user, host)
        Debug.debug_print(1, 'Shut down command: {}'.format(command))
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True)
        stdout, stderr = p.communicate()
        message = codecs.decode(stdout + stderr, 'utf-8')
        return self._json_response(message, 200)

    # noinspection PyTypeChecker
    def _save_settings(self, settings):
        """
        Save settings to disk.

        :param json settings: Settings in Json format.
        :rtype: str
        :returns: Status message

        """
        # Write settings to file
        self.write_settings_to_file(settings)
        Settings.load_settings_from_yaml()
        # Write all ssh key files to disk
        Main.populate_ssh_key_files()
        # Return status message
        message = 'Settings written to file'
        return self._json_response(message, 200)

    def _delete_param_value(self, param, value):
        """
        Remove a value from a parameter in the settings file.

        :param str param: Parameter to delete value from.
        :param str value: Value to delete.
        :rtype: str
        :returns: Status message

        """
        status = self.delete_param_value_from_file(
            param, value)
        Settings.load_settings_from_yaml()
        if status:
            message = "Value '{}' deleted from parameter '{}'"
        else:
            message = "Value '{}' NOT deleted from parameter '{}'"
        message = message.format(param, value)
        return self._json_response(message, 200)

    def _add_param_value(self, param, value):
        """
        Add value to a parameter in the settings file.

        :param str param: Parameter to add value to.
        :param str value: Value to add.
        :rtype: str
        :returns: Status message

        """
        self.add_param_value_to_file(
            param, value)
        Settings.load_settings_from_yaml()
        message = "Value '{}' added to parameter '{}'"
        message = message.format(param, value)
        return self._json_response(message, 200)

    # noinspection PyShadowingNames
    def _restart_ping(self):
        """
        Create a new crontab with ping commands

        :rtype: str
        :returns: Status message

        """
        Main.update_ping_crontab()
        message = 'Crontab updated'
        return self._json_response(message, 200)

    # noinspection PyUnboundLocalVariable
    def handle_request(self):
        """Web server function."""
        host = request.args.get('host')
        mac = request.args.get('mac')
        tab = request.args.get('tab')
        request_json = request.get_json()
        Debug.debug_print(3, "request_json: " + pprint.pformat(request_json))
        try:
            message = request.path
            if request.path == self.WEB_GUI_PATH:
                settings = self.render_settings_html()
                active_tab = 'about'
                if tab is not None:
                    active_tab = tab
                result = render_template(
                    'index.html', settings=settings, active_tab=active_tab,
                    restart_ping_path=Settings.WEB_API_PATH + 'restart_ping',
                    poweron_path=Settings.WEB_API_PATH + 'poweron',
                    poweroff_path=Settings.WEB_API_PATH + 'poweroff')
            elif request.path == self.WEB_API_PATH + 'poweron':
                message = 'poweron: mac={}'
                message = message.format(str(mac))
                result = self._poweron()
            elif request.path == self.WEB_API_PATH + 'poweroff':
                message = 'poweroff: host={}'
                message = message.format(str(host))
                result = self._poweroff()
            elif request.path == self.WEB_API_PATH + 'restart_ping':
                message = 'restart_ping'
                result = self._restart_ping()
            elif request.path == self.WEB_API_PATH + 'save_settings':
                message = 'save_settings'
                result = self._save_settings(request_json)
            elif request.path == self.WEB_API_PATH + 'delete_param_value':
                param = None
                value = None
                if 'param' in request_json:
                    param = request_json['param']
                if 'value' in request_json:
                    value = request_json['value']
                message = 'delete_param_value: param={}, value={}'
                message = message.format(param, value)
                result = self._delete_param_value(param, value)
            elif request.path == self.WEB_API_PATH + 'add_param_value':
                param = None
                if 'param' in request_json:
                    param = request_json['param']
                if 'value' in request_json:
                    value = request_json['value']
                message = 'add_param_value: param={}, value={}'
                message = message.format(param, value)
                result = self._add_param_value(param, value)
        except:
            error_log = LogFile(self.ERROR_LOG)
            error_log.write([message])
            traceback_message = traceback.format_exc()
            error_log.write([traceback_message], date_time=False)
            if Debug.debug > 0:
                Debug.debug_print(1, traceback_message)
                return self._json_response(traceback_message, 500)
            return self._json_response('Internal system error!', 500)
        message_log = LogFile(self.MESSAGE_LOG)
        message_log.write([message])
        return result


class Main(Settings):
    """Contains the script"""

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.

        :rtype: Namespace

        """
        debug_help = 'Debugging printout level.'
        no_ping = ('If this option is supplied, no ping cron jobs will be adde'
                   'd att container start.')
        port_help = 'Port the web server runs on.'
        description = 'Start Zipato extension web server.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('-n', '--no_ping', dest='ping',
                            action='store_false', help=no_ping)
        parser.set_defaults(ping=True)
        parser.add_argument('--debug', type=int, default=0,
                            help=debug_help, required=False)
        parser.add_argument('-p', '--port', type=int,
                            help=port_help, required=False)
        args = parser.parse_args()
        return args

    # noinspection PyShadowingNames
    @staticmethod
    def update_ping_crontab():
        """
        Create a new crontab with ping commands

        :raises: ZipatoError

        """
        ping_commands = []
        for host in Settings.PING_HOSTS:
            ping_command = '{} /usr/bin/python3 {}ping.py --host {} >> {} 2>&1'
            ping_command = ping_command.format(Settings.PING_SCHEDULE,
                                               Settings.PROGRAM_PATH,
                                               copy(host),
                                               Settings.ERROR_LOG)
            ping_commands.append(copy(ping_command))
        cron_lines = '\n'.join(ping_commands)
        cron_command = '(echo "{}") | crontab -'.format(cron_lines)
        p = subprocess.Popen(
            cron_command, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        if stderr is not None:
            message = (
                'Error updating crontab!\nStandard in:\n{}\nStandard out:\n{}')
            message = message.format(str(stdout), str(stderr))
            raise ZipatoError(message)

    @staticmethod
    def populate_ssh_key_files():
        """
        Read all ssh key file contents from settings and write ssh key file(s)
        to disk for SSH to use.

        """
        for host, values in Settings.API_POWEROFF_HOSTS.items():
            file_name = Settings.SSH_KEY_FILE.replace('$HOST', host)
            file_obj = open(file_name, 'w')
            file_obj.writelines(values['ssh_key'])
            file_obj.close()
            command = "chmod 0600 {}".format(file_name)
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            p.communicate()
        message = "The following ssh key files have been written to disk:\n{}"
        Debug.debug_print(
            2, message.format(str(Settings.API_POWEROFF_HOSTS.keys())))

    def run(self):
        """
        Run the script.
        
        """
        self.populate_ssh_key_files()
        args = self._parse_command_line_options()
        Settings.DEBUG = Debug.DEBUG = args.debug
        if args.ping:
            self.update_ping_crontab()
        if args.port is not None:
            Settings.TCP_PORT = args.port
        flask_debug = False
        if args.debug > 0:
            flask_debug = True
        zipatoserver.run(
            debug=flask_debug,
            host='0.0.0.0',
            port=self.TCP_PORT,
            processes=self.PROCESSES)

zipatoserver = Flask(__name__,
                     static_url_path="",
                     static_folder='html_static',
                     template_folder='html_templates')
Settings.static_init()
Settings.load_settings_from_yaml()


@zipatoserver.route(Settings.WEB_GUI_PATH)
@zipatoserver.route(Settings.WEB_API_PATH + 'poweron')
@zipatoserver.route(Settings.WEB_API_PATH + 'poweroff')
@zipatoserver.route(Settings.WEB_API_PATH + 'save_settings', methods=['POST'])
@zipatoserver.route(Settings.WEB_API_PATH + 'restart_ping', methods=['POST'])
@zipatoserver.route(Settings.WEB_API_PATH + 'delete_param_value',
                    methods=['DELETE'])
@zipatoserver.route(Settings.WEB_API_PATH + 'add_param_value', methods=['PUT'])
def index():
    """Handle incoming HTTP requests."""
    request_handler = ZipatoRequestHandler()
    return request_handler.handle_request()

if __name__ == '__main__':
    main = Main()
    main.run()
