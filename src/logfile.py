# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Log file
********

This module handles connections to a log file. It will lock the

"""

import datetime
import fcntl
import time


class LogFile:
    """Log file container."""

    def __init__(self, file_name, verbosity):
        """
        Initializes a LogFile instance.

        :param str file_name: File name and full path to log file.
        :param int verbosity: Log file verbosity.

        """
        self._file_name = file_name
        self._verbosity = verbosity

    def write(self, lines, level=0, date_time=True):
        """
        Write message to log file.

        :param list lines: List of messages.
        :param int level: Required verbosity level for lines to be added to
                          log file.
        :param bool date_time: If date and time should be added to message.

        """
        if level >= self._verbosity:
            if date_time:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lines = [now+' '+i for i in lines]
            lines = [i+'\n' for i in lines]
            file_obj = open(self._file_name, 'a')
            fcntl.flock(file_obj, fcntl.LOCK_EX)
            lock = False
            for i in range(40):
                try:
                    fcntl.flock(file_obj, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = True
                    break
                except IOError:
                    time.sleep(0.05)
            if lock:
                file_obj.writelines(lines)
                file_obj.close()
