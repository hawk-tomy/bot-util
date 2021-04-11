import logging


from .config import config
from .data import data


logging.getLogger(__name__).addHandler(logging.NullHandler())