from __future__ import annotations


from typing import Optional


from discord import ButtonStyle ,Colour, Embed, Interaction, Message, ui
from discord.abc import Messageable
from discord.ext import menus
from discord.ext.commands import Context as _Context

__all__ = ('Context', )


class Confirm(ui.View):
    def __init__(self, embed: Embed= None, timeout: int=None):
        super().__init__(timeout=timeout, delete_message_after=True)
        self.result = None
        self.embed = embed

    async def send(self, ctx: Context):
        msg = await ctx.send(embed=self.embed, view=self)
        await self.wait()
        for item in self.children:
            item.disabled = True
        await msg.edit(embed=self.embed, view=self)
        return self.result

#    async def on_error(self, error: Exception, item: ui.Item, interaction: Interaction) -> None:
#        pass
#
    @ui.button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('Confirming')
        self.value = True
        self.stop()

    @ui.button(label='ancel', style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('Cancelling')
        self.value = False
        self.stop()


#class Confirm(menus.Menu):
#    def __init__(self, title: str, description: str= None, timeout: int=None):
#        super().__init__(timeout=timeout, delete_message_after=True)
#        self.result = None
#        self.title = title
#        self.description = description
#
#    async def send(self, ctx)-> Optional[bool]:
#        await self.start(ctx, wait=True)
#        return self.result
#
#    async def send_initial_message(self, ctx: Context, channel: Messageable):
#        return await channel.send(embed=ctx._confirm(title=self.title, description=self.description))
#
#    @menus.button('\u2705')
#    async def ok(self, payload):
#        self.result = True
#        self.stop()
#
#    @menus.button('\u274c')
#    async def no(self, payload):
#        self.result = False
#        self.stop()


class Context(_Context):
    def __init__(self, **attrs):
        self.invoked_error = False
        super().__init__(**attrs)

    @property
    def invoked_error(self)-> bool:
        return self.__invoked_error and self.command_failed

    @invoked_error.setter
    def invoked_error(self, value: bool):
        self.__invoked_error = bool(value)

    def _success(self, title: str, description: str= None)-> Embed:
        return Embed(title=f'\u2705 {title!s}', description=description if description is not None else '', colour=Colour.green())

    def _error(self, title: str, description: str= None)-> Embed:
        return Embed(title=f'\u26a0 {title!s}', description=description if description is not None else '', colour=Colour.dark_red())

    def _info(self, title: str, description: str= None)-> Embed:
        return Embed(title=f'\u2139\ufe0f {title!s}', description=description if description is not None else '', colour=Colour.blue())

    def _confirm(self, title: str, description: str= None)-> Embed:
        return Embed(title=f'\u2754 {title!s}', description=description if description is not None else '', color=Colour.gold())

    async def embed(self, embed: Embed, **kwargs)-> Message:
        return await self.send(embed=embed, **kwargs)

    async def re_embed(self, embed: Embed, **kwargs)-> Message:
        return await self.reply(embed=embed, **kwargs)

    async def success(self, title: str, description: str = None, **kwargs)-> Message:
        return await self.embed(
            self._success(title=title, description=description), **kwargs)

    async def re_success(self, title: str, description: str = None, **kwargs) -> Message:
        return await self.re_embed(self._success(title=title, description=description,), **kwargs)

    async def error(self, title: str, description: str = None, **kwargs)-> Message:
        return await self.embed(self._error(title=title, description=description), **kwargs)

    async def re_error(self, title: str, description: str = None, **kwargs)-> Message:
        return await self.re_embed(self._error(title=title, description=description), **kwargs)

    async def info(self, title: str, description: str = None, **kwargs)-> Message:
        return await self.embed(self._info(title=title, description=description), **kwargs)

    async def re_info(self, title: str, description: str = None, **kwargs)-> Message:
        return await self.re_embed(self._info(title=title, description=description), **kwargs)

    async def confirm(self, title: str, description: str= None, timeout: int=None)-> Optional[bool]:
        return await Confirm(embed=self._confirm(title=title, description=description), timeout=timeout).send(self)
