import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
import os


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["h", "H"], help = 'help <category>/<cmd>')
    async def help(self, ctx, coges = None):
        found = False
        pref = await get_prefixes(ctx)
        if coges == None:
            comms = ''
            i = 0
            emb = discord.Embed(title='Help', description=f'Use `{pref}help <cmd>` for more info\nYou can also use `{pref}help <category>` for more info on a category.', color = discord.Colour.blurple())
            emb.set_footer(text='My commands', icon_url=self.bot.user.avatar_url)
            cogl = self.bot.coglist
            if cogl == "Help":
                cogl.remove('Help')
            num = len(cogl)
            while i < num:
                cog = self.bot.get_cog(cogl[i])
                comma = cog.get_commands()
                for co in comma:
                    if not co.hidden:
                        comms += f'`{co.name}`  '
                    else:
                        comms += '`**скрыто**`'
                emb.add_field(name=f'__{cogl[i]}__', value=f'{comms}', inline=False)
                comms = ''
                i += 1
            await ctx.send(embed=emb)
        else:
            try:
                colis = ''
                cog = [coges]
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    colis += f'•`{c.name}` — `{pref}{c.help}`\n'
                halp=discord.Embed(title=f'Command Listing\n{self.bot.cogs[coges].__doc__}', description=f'{colis}', color = discord.Colour.blurple())
                await ctx.send('',embed=halp)
            except:
                comms = ''
                i = 0
                cogl = self.bot.coglist
                num = len(cogl)
                while i < num:
                    cog = self.bot.get_cog(cogl[i])
                    comma = cog.get_commands()
                    for co in comma:
                        if str(co) == str(coges):
                            comms += f'**Command**\n```{co.name}```\n**Syntax** ```{pref}{co.help}```\n**Aliases**```{co.aliases}```'
                            found = True
                    i += 1
                if not found:
                    emb = discord.Embed(title='Ooops!',description='How do you even use "'+coges+'"?',color=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(description=f'{comms}', color = discord.Colour.blurple())
                    emb.set_footer(text='My commands', icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Help(bot))