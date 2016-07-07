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

    __CONFIG_FILE = 'zipatoserver.conf'
    """(*str*) Config file name."""

    __PATH_WITH_SLASH_PARAMETERS = [
        'HTTP_PATH', 'WAKEONLAN_PATH', 'PING_PATH', 'SSH_PATH']
    """(*list*) Parameters in this list with always end with a slash."""

    __PATH_WITHOUT_SLASH_PARAMETERS = ['LOG_FILE_NAME', 'SSH_KEY_FILE']
    """(*list*) Parameters in this list will never end with a slash."""

    def load_settings_from_yaml(self):
        """Set all system constants from YAML file."""
        with open(self.__CONFIG_FILE, 'r') as f:
            constants = yaml.load(f)
        for constant, value in constants:
            if constant in self.__PATH_WITH_SLASH_PARAMETERS:
                Settings.__dict__[constant] = self._format_path(value, True)
            elif constant in self.__PATH_WITHOUT_SLASH_PARAMETERS:
                Settings.__dict__[constant] = self._format_path(value, False)
            else:
                Settings.__dict__[constant] = value

    @staticmethod
    def _format_path(self, path, slash=True):
        """
        Format a path string.

        :param str path: Path to format.
        :param bool slash: If the path string should end with a slash
        :rtype: str
        :return: A formatted path string.

        """
        if len(path) == 0:
            return path
        elif slash and path[-1] != '/':
            return path + '/'
        elif not slash and path[-1] == '/':
            return path[:-1]
        else:
            return path
