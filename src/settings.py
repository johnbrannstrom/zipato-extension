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

    def load_settings_from_yaml(self):
        """Set all system constants from YAML file."""
        with open('zipatoserver.conf', 'r') as f:
            constants = yaml.load(f)
        for constant, value in constants:
            Settings.__dict__[constant] = value
