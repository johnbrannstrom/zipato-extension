# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Error
******

This module contains exceptions.

"""


class ZipatoError(Exception):

    def __init__(self, message):
        """
        Constructor function.

        :param str message:

        """
        self._message = message

    def __str__(self):
        """
        String function.

        """
        return self._message

