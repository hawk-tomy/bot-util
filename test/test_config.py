from dataclasses import asdict, dataclass


from bot_util import config

@dataclass
class NameTest:
    name: str = 'test_name'

@dataclass
class AgeTest:
    age: int = 20

config.add_default_config(key='name_test',data=NameTest)
config.add_default_config(key='age_test',data=AgeTest())
config.load_config()
print(config)
print(dir(config))
print({k:asdict(v) for k,v in config.items()})
