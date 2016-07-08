# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Log file
********

This module contains a log file representation class.

"""

import datetime


class LogFile:
    """Log file container."""

    def __init__(self, name):
        """Initializes a LogFile instance."""
        self.file = open(name, 'a+')

    def write(self, message, date_time=True):
        """
        Write message to log file.

        :param str message: Log message.
        :param bool date_time: If date and time should be added to message.

        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if date_time:
            message = now + ' ' + message
        message += '\n'
        self.file.write(message)

    def close(self):
        """Close log file."""
        self.file.close()
