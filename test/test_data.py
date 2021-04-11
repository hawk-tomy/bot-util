from dataclasses import dataclass

from bot_util import data

@dataclass
class test1:
    name: str

@dataclass
class test2:
    age: int

data.add_dataclass('test',test1).add_dataclass('test2',test2)

print(dir(data))
print(data.test1)
print(data.test)
data.save_test()
print('save')
input('pls any key...')
data.reload_test()
print('reload')
print(data.test)

print(data.test2)
data.save_test2()
print('save')
input('pls any key...')
data.reload_test2()
print('reload')
print(data.test2)
