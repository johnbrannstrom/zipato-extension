#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import argparse

class Main(Settings):
  """Contains the script."""

    def ping(self, host):
        """
        Ping a node and set Zipato status.
        
        :param str host: Target host.
        :rtype: str
        :returns: Status message
        """
        host = request.args.get('host')
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
      
      
    def run(self):
        """Run the script"""
        args = self._parse_command_line_options()
        Settings.load_settings_from_yaml(settings_path='/etc/')
        Settings.DEBUG = args.debug

if __name__ == '__main__':
    main = Main()
    main.run()
