# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Zipato Connection
*****************

This module handles connections to the Zipato cloud.

"""


import requests
from settings import Settings

class ZipatoConnection(Settings):

    def __init__(self, serial):
        """
        Initializes a ZipatoConnection.
    
        :param str serial: Zipato Box serial.
    
        """
        self.serial = serial
    
    def set_sensor_status(self, ep, apikey, status):
       """
       Set status of a sensor.
       
       :param str ep: Target ep.
       :param str ep: Target apikey.
       :param bool ep: Status value to set the sensor to.
       :rtype: int
       :returns: Status of the HTTP request to the Zipato cloud.
       
       """
       command = ("https://my.zipato.com/zipato-web/remoting/attribute/se"
                  "t?serial={}&ep={}&apiKey={}&state={}")
       command = command.format(self.ZIPATO_SERIAL, ep, apikey, str(status))
       response = requests.get(command)
       return response.status_code
>>>>>>> origin/devel
