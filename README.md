[discord.py]: https://github.com/Rapptz/discord.py
[discord-ext-menus]: https://github.com/Rapptz/discord-ext-menus
[dispander]: https://github.com/DiscordBotPortalJP/dispander
[pyyaml]: https://github.com/yaml/pyyaml
[dataclasses]: https://docs.python.org/ja/3/library/dataclasses.html

# TL;DR

bot用の便利関数などをまとめたパッケージのリポジトリです。
個人的に便利で複数のBOTで利用するであろう機能をまとめています。

# 機能

以下アルファベット順に。

## config

ビルトインパッケージの[dataclasses]を利用したconfig管理機能です。configは自動的にカレントディレクトリの`config.yaml`に保存されます。

使用例
```py
from dataclasses import dataclass
from bot_util.config import config, ConfigBase

@dataclass
class MyBotSetting(ConfigBase):
    sending_channel_id: int= None

config.add_default_config(MyBotSetting, key='setting')
print(config.setting)
#MyBotSetting(sending_channel_id=None)
```

## data

[dataclasses]と[yaml][pyyaml]を利用したdata管理機能です。dataはカレントディレクトリの`data`フォルダの`.yaml`または、`.yml`から読み込まれます。

## dispander

[dispander]をもとに改変を加えています。使い方は変化していないので、
[dispander]を参照してください。

### originalからの変更点

- cogとしての機能を削除
- 送信を決める対象を変更(bug?)
- 埋め込みのcolorを指定(configで変更可能)

## help_command

BOTのヘルプを表示するためのクラスが記述されています。BOT定義時に呼び出して、インスタンスを渡すことで利用可能です。埋め込みのcolorをconfigから指定できます。

## menus

[discord-ext-menus]のクラスをもとに、メッセージ送信時も特定の関数が呼び出されるようなクラスを用意し、discord.ext.menusの全てをimportしています。

| original class | message ver |
|---|---|
| Menu | MsgMenu |
| MenuPages | MsgMenuPages |

# 利用しているパッケージ

- [discord.py]
- [discord-ext-menus]
- [dispander]
- [pyyaml]
