from __future__ import annotations


from .config_parser import ConfigBase, ConfigParser


__all__ = ('config', 'ConfigBase')


config = ConfigParser('config.yaml')
