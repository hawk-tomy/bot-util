from __future__ import annotations


from dataclasses import dataclass
from os import getenv


if int(getenv('BOT_UTIL_CONFIG_ENABLED', 1)):
    from .config import config, ConfigBase

    @dataclass
    class EmbedSetting(ConfigBase):
        color: int= 0x54c3f1

    config.add_default_config(EmbedSetting, key='embed_setting')
else:
    pass
