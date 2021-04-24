from dataclasses import dataclass


from .config import config, ConfigBase


@dataclass
class EmbedColor(ConfigBase):
    color: int= 0x54c3f1


config.add_default_config(EmbedColor, key='embed_color')
