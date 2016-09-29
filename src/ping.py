#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import argparse

class Main(Settings):
  """Contains the script."""

    def ping(self, host):
        """
        Ping one host and set status to a Zipato sensor.
        
        :param str host: Target host.
        :rtype: str
        :returns: Status message
        """
        if host in self.API_PING_HOSTS.keys():
            ep = self.API_PING_HOSTS[host]['ep']
            apikey = self.API_PING_HOSTS[host]['apikey']
        else:
            message = "ping host={}, status='Host has not been configured for ping'"
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
            sleep(self.PING_INTERVAL)
        # Set the status of a Zipato sensor to the ping status
        command = ("https://my.zipato.com/zipato-web/remoting/attribute/se"
                   "t?serial={}&ep={}&apiKey={}&state={}")
        zipato_connection = ZipatoConnection(self.ZIPATO_SERIAL)
        if ping_ok:
            zipato_connection.set_sensor_status(ep=ep, apikey=apikey, status='true')
        else:
            zipato_connection.set_sensor_status(ep=ep, apikey=apikey, status='false')
        self.debug_print(10, command, 'zipatoserver', 'ZipatoServer', '_ping')
        zipato_connection.set_sensor_status(ep=ep, apikey=apikey, status)
        message = 'ping host={}, status={}'.format(host, status)
      
      
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
        parser.add_argument('-o, '--host', type=str, help=host_help, required=True)
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
        self._ping(host)

if __name__ == '__main__':
    main = Main()
    main.run()
