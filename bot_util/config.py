from __future__ import annotations


from dataclasses import asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Any, NewType, NoReturn, Union


import yaml


logger = logging.getLogger(__name__)


D = NewType('dataclass',Any)
C = dict[str, D]


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


@dataclass
class __Config:
    __default_config: C = field(default_factory=dict)
    __config: Union[C, None] = None

    @property
    def default_config(self)-> dict:
        default_config = dict()
        for k,d in self.__default_config.items():
            default_config[k] = asdict(d)
        return default_config

    @property
    def config(self)-> C:
        if self.__config is None:
            self.load_config()
        return self.__config

    def __getitem__(self,key)-> Union[D,NoReturn]:
        if isinstance(key,str):
            return self.config[key]
        else:
            raise KeyError

    def items(self):
        return self.config.items()

    def add_default_config(self, key: str, data: D)-> __Config:
        if not is_dataclass(data):
            raise TypeError('data must be instance or class of dataclass.')
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if isinstance(data, type):
            data = data()
        self.__default_config[key] = data
        return self

    def __set_config(self, config: dict[str,Union[dict,list]])-> None:
        new_config = dict()
        for k,v in config.items():
            if k not in self.__default_config:
                continue
            if isinstance(v,list):
                v = self.__default_config[k].__class__(*v)
            elif isinstance(v,dict):
                v = self.__default_config[k].__class__(**v)
            new_config[k] = v
        self.__config = new_config

    def load_config(self)-> None:
        if Path('./config.yaml').exists():
            with open('./config.yaml')as f:
                self.__set_config(yaml.safe_load(f))
        else:
            logger.warning(f'create config.yaml file')
            with open('./config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)
            self.__set_config(self.default_config)


config = __Config()
