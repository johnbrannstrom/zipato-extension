import requests

class ZipatoConnection(Settings):

    __init__(self, serial):
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
       
       """
       
