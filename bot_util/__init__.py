import logging


from . import util
from .util import *


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }

__all__ = ('YAML_DUMP_CONFIG',) + util.__all__
logging.getLogger(__name__).addHandler(logging.NullHandler())
