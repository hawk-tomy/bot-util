from __future__ import annotations


from dataclasses import asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Callable


import yaml


from . import YAML_DUMP_CONFIG


__all__ = ('DataParser','DataBase')
logger = logging.getLogger(__name__)
class DataBase:pass
D = dict[str, DataBase]


@dataclass
class DataParser:
    _path: str = './data'
    __dataclass: D = field(default_factory=dict)
    __names: set[str] = field(default_factory=set)
    __reload_funcs: list[Callable] = field(default_factory=list)
    __save_funcs: list[Callable] = field(default_factory=list)

    def __pre_init__(self):
        self._path = Path(self._path)

    def __getattr__(self, name):
        self.load_data()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError

    def load_data(self)-> None:
        if not self._path.exists():
            self._path.mkdir()
            logger.warning(f'create data dirctory')
        for p in self._path.iterdir():
            if not p.is_file() or p.suffix not in ('.yaml','.yml'):
                continue
            self._setter(p)

    def _setter(self,p: Path)-> None:
        name = p.stem
        if name.startswith('_') or name in self.__names:
            return
        self.__names.add(name)
        cls = self.__dataclass.get(name,None)

        def loader()-> DataBase:
            with p.open()as f:
                value = yaml.safe_load(f)
            if cls is not None:
                value = cls(**value)
            return value

        value: DataBase = loader()

        def getter(self)-> DataBase:
            return value

        def save_func(self)-> None:
            with p.open('w')as f:
                yaml.dump(asdict(value),f,**YAML_DUMP_CONFIG)

        def reload_func(self)-> None:
            nonlocal value
            value = loader()

        self.__reload_funcs.append(reload_func)
        self.__save_funcs.append(save_func)

        setattr(self.__class__,name,property(getter))
        setattr(self.__class__,f'save_{name}',save_func)
        setattr(self.__class__,f'reload_{name}',reload_func)

    def add_dataclass(self, key: str, data: D)-> DataParser:
        data = data if isinstance(data, type) else type(data)
        if not is_dataclass(data) or not issubclass(data, DataBase):
            raise TypeError('data must be instance or class of dataclass.')
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        self.__dataclass[key] = data
        return self

    def all_reload(self):
        for func in self.__reload_funcs:
            func(self)

    def all_save(self):
        for func in self.__save_funcs:
            func(self)
