#!/usr/bin/python3

import subprocess
import requests
import re
import datetime
from time import sleep
from flask import Flask
from flask import request

# The service will respond to requests on this port
tcpPort = 5000

# The service will respons to requests on this HTTP path
httpPath = '/'

# Sets if debug mode should be used
debug = False

# Set if logging should be used
logging = True

# Full path and name of log file
logFileName = '/home/john/httpaction'

# Path to the wakeonlan command
wakeonlanPath = '/usr/bin/'

# Path to the ping command
pingPath = '/bin/'

# Number of pings
pingCount = 3

# Path to the ssh command
sshPath = '/usr/bin/'

# Path to ssh key directory
sshKeyPath = '/home/john/.ssh/id_rsa'

httpaction = Flask(__name__)


class LogFile():
    def __init__(self, name):
        self.file = open(name, 'a+')

    def write(self, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = now + ' ' + message + '\n'
        self.file.write(line)

    def close(self):
        self.file.close()


@httpaction.route(httpPath)
def index():
    def poweron():
        if mac != None:
            if host != None:
                command = "{}wakeonlan -i {} {}".format(wakeonlanPath, host, mac)
            else:
                command = "{}wakeonlan {}".format(wakeonlanPath, mac)
            for i in range(3):
                p = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True)
                stdout, stderr = p.communicate()
                sleep(0.1)
            if logging:
                logFile.write(command)
            return stdout + stderr
        else:
            return "Action 'poweron' must have parameter 'mac'!"

    def poweroff():
        if user != None and host != None:
            command = "{}ssh -i {} -T {}@{} 'shutdown -h now'"
            command = command.format(sshPath, sshKeyPath, user, host)
            p = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
            stdout, stderr = p.communicate()
            if logging:
                logFile.write(command)
            return stdout + stderr
        elif user == None:
            return "Action 'poweroff' must have parameter 'user'!"
        elif host == None:
            return "Action 'poweroff' must have parameter 'host'!"

    def ping():
        if host != None:
            for i in range(pingCount):
                command = "{}ping -c {} {}".format(pingPath, str(pingCount), host)
                p = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True)
                stdout, stderr = p.communicate()
                if logging:
                    logFile.write(command)
                result = re.match('.*0 received.*', str(stdout), re.DOTALL)
                pingOk = result == None
                if pingOk:
                    break
                sleep(5)
            if serial != None and ep != None and apiKey != None:
                # Set the status of a Zipato sensor to the ping status
                command = "https://my.zipato.com/zipato-web/remoting/attribute/set?serial={}&ep={}&apiKey={}&state={}"
                if pingOk:
                    command = command.format(serial, ep, apiKey, 'true')
                else:
                    command = command.format(serial, ep, apiKey, 'false')
                r = requests.get(command)
                if logging:
                    logFile.write(command)
                return str(r.status_code)
            else:
                # Just return a the ping status
                if pingOk:
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
    apiKey = request.args.get('apiKey')
    if logging:
        logFile = LogFile(logFileName)
    if action.lower() == 'poweron':
        result = poweron()
    elif action.lower() == 'poweroff':
        result = poweroff()
    elif action.lower() == 'ping':
        result = ping()
    else:
        result = "Unknown value '{}' for paramater 'action'. Choose from 'poweron, poweroff, ping'!".format(action)
    if logging:
        logFile.close()
    return result


if __name__ == '__main__':
    httpaction.run(debug=debug, host='0.0.0.0', port=tcpPort, threaded=True)