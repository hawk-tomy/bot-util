import os
import logging


import yaml


logger = logging.getLogger(__name__)


HARD_CORDING_DEFAULT_CONFIG = dict()
YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


class __Config:
    def __init__(self):
        self.__default_config = HARD_CORDING_DEFAULT_CONFIG
        self.__config = None

    @property
    def default_config(self):
        return self.__default_config

    def __getitem__(self,key):
        if isinstance(key,str):
            if self.__config is None:
                self.load_config()
            return self.__config[key]
        else:
            raise KeyError

    def load_config(self):
        if not os.path.isdir('./data'):
            os.mkdir('./data')
            logger.warning(f'create data dirctory')

        if os.path.isfile('./data/default_config.yaml'):
            with open('./data/default_config.yaml')as f:
                self.default_config =  yaml.safe_load(f)
        else:
            logger.warning(f'create data/default_config.yaml file')
            with open('./data/default_config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)

        if os.path.isfile('./config.yaml'):
            with open('./config.yaml')as f:
                self.__config = yaml.safe_load(f)
        else:
            logger.warning(f'create config.yaml file')
            with open('./config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)
            self.__config = self.default_config


config = __Config()
