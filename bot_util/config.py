from __future__ import annotations


from os import getenv


from .config_parser import ConfigBase, ConfigParser


__all__ = ('config', 'ConfigBase')


if int(getenv('BOT_UTIL_CONFIG_ENABLED', 1)):
    config = ConfigParser('config.yaml')
