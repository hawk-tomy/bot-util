import logging


from .config import config


logging.getLogger(__name__).addHandler(logging.NullHandler())