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

    def write(self, message):
        """
        Write line to log file.

        :param str message: Log message.

        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = now + ' ' + message + '\n'
        self.file.write(line)

    def close(self):
        """Close log file."""
        self.file.close()
