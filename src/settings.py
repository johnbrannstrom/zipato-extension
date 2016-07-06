# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Settings
********

This module contains settings.

"""

import yaml


class Settings:
    """Settings container."""

    @staticmethod
    def load_settings_from_yaml():
        """Set all system constants from YAML file."""
        with open('zipatoserver.conf', 'r') as f:
            constants = yaml.load(f)
        for constant, value in constants:
            if constant == 'HTTP_PATH':
                self._HTTP_PATH = value
            else:
            Settings.__dict__[constant] = value

    _HTTP_PATH = None
    @property
    def HTTP_PATH(self):
        if len(self._HTTP_PATH) == 0 or self._HTTP_PATH[-1] == '/':
            return self._HTTP_PATH
        else:
            return self._HTTP_PATH + '/'
