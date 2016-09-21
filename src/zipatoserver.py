#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import requests
import re
import argparse
import traceback
import json
import codecs
from time import sleep
from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from settings import Settings
from logfile import LogFile
from debug import Debug


class ZipatoServer(Settings, Debug):
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
        message = codecs.decode(stdout + stderr, 'utf-8')
        return self._json_response(message, 200)

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
        command = "{}ssh -i {} -T {}@{} 'shutdown -h now'"
        ssh_key_file = self.API_POWEROFF_HOSTS[host]['ssh_key_file']
        command = command.format(self.SSH_PATH, ssh_key_file, user, host)
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True)
        stdout, stderr = p.communicate()
        message = codecs.decode(stdout + stderr, 'utf-8')
        return self._json_response(message, 200)

    # noinspection PyShadowingNames
    def _ping(self):
        """
        Ping a node and set Zipato status.

        :rtype: str
        :returns: Status message

        """
        host = request.args.get('host')
        if host is None:
            message = "Error 'ping' must have parameter 'host'!"
            return self._json_response(message, 400)
        if host in self.API_PING_HOSTS.keys():
            ep = self.API_PING_HOSTS[host]['ep']
            apikey = self.API_PING_HOSTS[host]['apikey']
        else:
            message = "Error host '{}' has not been configured for 'ping'!"
            message = message.format(host)
            return self._json_response(message, 400)
        for i in range(self.PING_COUNT):
            command = "{}ping -c {} {}"
            command = command.format(self.PING_PATH, str(self.PING_COUNT), host)
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
        # Set the status of a Zipato sensor to the ping status
        command = ("https://my.zipato.com/zipato-web/remoting/attribute/se"
                   "t?serial={}&ep={}&apiKey={}&state={}")
        if ping_ok:
            command = command.format(serial, ep, apikey, 'true')
        else:
            command = command.format(serial, ep, apikey, 'false')
        self.debug_print(10, command, 'zipatoserver', 'ZipatoServer', '_ping')
        r = requests.get(command)
        status_code = r.status_code
        if status_code == 200:
            message = 'Zipato ping status was updated'
        else:
            message = 'Zipato ping status could not be updated'
        return self._json_response(message, status_code)

    # noinspection PyTypeChecker
    def _save_settings(self, settings):
        """
        Save settings to disk.

        :param json settings: Settings in Json format.
        :rtype: str
        :returns: Status message

        """
        self.write_settings_to_file(settings, settings_path='/etc/')
        Settings.load_settings_from_yaml(settings_path='/etc/')
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
            param, value, settings_path='/etc/')
        Settings.load_settings_from_yaml(settings_path='/etc/')
        if status:
            message = "Value '{}' deleted from parameter '{}'"
        else:
            message = "Value '{}' NOT deleted from parameter '{}'"
        message = message.format(param, value)
        return self._json_response(message, 200)

    def handle_request(self):
        """Web server function."""
        user = request.args.get('user')
        host = request.args.get('host')
        mac = request.args.get('mac')
        tab = request.args.get('tab')
        response_json = request.get_json()
        try:
            message = request.path
            if request.path == self.WEB_GUI_PATH:
                settings = self.render_settings_html(settings_path='/etc/')
                result = render_template(
                    'index.html', settings=settings, active_tab=tab,
                    ping_path=Settings.WEB_API_PATH + 'ping',
                    poweron_path=Settings.WEB_API_PATH + 'poweron',
                    poweroff_path=Settings.WEB_API_PATH + 'poweroff')
            elif request.path == self.WEB_API_PATH + 'poweron':
                message = 'poweron: mac={}'
                message = message.format(str(mac))
                result = self._poweron()
            elif request.path == self.WEB_API_PATH + 'poweroff':
                message = 'poweroff: user={}, host={}'
                message = message.format(str(user), str(host))
                result = self._poweroff()
            elif request.path == self.WEB_API_PATH + 'ping':
                message = 'ping: host={}'
                message = message.format(str(host))
                result = self._ping()
            elif request.path == self.WEB_API_PATH + 'save_settings':
                message = 'save_settings'
                result = self._save_settings(response_json)
            elif request.path == self.WEB_API_PATH + 'delete_param_value':
                param = None
                value = None
                if 'param' in response_json:
                    param = response_json['param']
                if 'value' in response_json:
                    value = response_json['value']
                message = 'delete_param_value: param={}, value={}'
                message = message.format(param, value)
                result = self._delete_param_value(param, value)
        except:
            error_log = LogFile(self.ERROR_LOG)
            error_log.write(message)
            traceback_message = traceback.format_exc()
            error_log.write(traceback_message, date_time=False)
            error_log.close()
            if self.DEBUG > 0:
                return self._json_response(traceback_message, 500)
            return self._json_response('Internal system error!', 500)
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
        debug_help = 'Debugging printout level.'
        description = 'Start Zipato extension web server.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--debug', type=int, default=0,
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args

    def run(self):
        """Run the script"""
        args = self._parse_command_line_options()
        Settings.DEBUG = args.debug
        flask_debug = False
        if args.debug > 0:
            flask_debug = True
        zipatoserver.run(
            debug=flask_debug,
            host='0.0.0.0',
            port=self.TCP_PORT,
            processes=self.PROCESSES)


Settings.load_settings_from_yaml(settings_path='/etc/')
zipatoserver = Flask(__name__,
                     static_url_path="",
                     static_folder='html_static',
                     template_folder='html_templates')


@zipatoserver.route(Settings.WEB_GUI_PATH)
@zipatoserver.route(Settings.WEB_API_PATH + 'poweron')
@zipatoserver.route(Settings.WEB_API_PATH + 'poweroff')
@zipatoserver.route(Settings.WEB_API_PATH + 'ping')
@zipatoserver.route(Settings.WEB_API_PATH + 'save_settings', methods=['POST'])
@zipatoserver.route(Settings.WEB_API_PATH + 'delete_param_value',
                    methods=['DELETE'])
@zipatoserver.route(Settings.WEB_API_PATH + 'add_param_value', methods=['PUT'])
def index():
    """Handle incoming HTTP requests."""
    web_server = ZipatoServer()
    return web_server.handle_request()

if __name__ == '__main__':
    main = Main()
    main.run()
