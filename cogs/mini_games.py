import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *

class _Minigames_(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["рандом"])
    async def random(self, ctx, *, arg=None):
        if arg == None:
            rand = random.randint(0, 100)
            emb = discord.Embed(title=f'Выпало число: __{str(rand)}__')
            await ctx.send(embed=emb)
        elif arg != None:
            atr = arg.split('/ ')
            num = len(atr)
            rand = random.randint(0, num-1)
            emb = discord.Embed(title=f'Выпало: __{atr[rand]}__')
            await ctx.send(embed=emb)
    @commands.command(aliases=["перестрелка"])
    async def shootout(self, ctx, user1, user2, ammo1, ammo2):
            chance = 50
            if int(ammo1) - int(ammo2) >= 5 and int(ammo1) - int(ammo2) < 15:
                chance = chance + 15
            elif int(ammo1) - int(ammo2) >= 15:
                chance = chance + 25
            elif int(ammo2) - int(ammo1) >= 5 and int(ammo2) - int(ammo1) < 15:
                chance = chance - 15
            elif int(ammo2) - int(ammo1) >= 15:
                chance = chance - 25
            else:
                chance = chance
            win = random.randint(0, 100)
            await ctx.send('Шанс выигрыша: ' + str(chance) + '/' + str(100-int(chance)))
            if win < chance:
                await ctx.send('Выиграл ' + user1 + '!')
            elif win == chance:
                await ctx.send('Ничья!')
            else:
                await ctx.send('Выиграл ' + user2 + '!')
    @commands.command(aliases=["дуэль"])
    async def duel(self, ctx, user1, user2):
        await ctx.send('Шансы 50/50')
        win = random.randint(0, 100)
        if win < 50:
            await ctx.send('Выиграл ' + user1 + '!')
        elif win == 50:
            await ctx.send('Ничья!')
        else:
            await ctx.send('Выиграл ' + user2 + '!')
    @commands.command(name="CookeGame", aliases=["CG", "cg"])
    async def CookeGame(self, ctx):
        emb = discord.Embed(title='Игра "Печенька"', color=discord.Colour.orange())
        emb.add_field(name='Правила', value='Кто первый нажмёт на реакцию - победил!')
        mess = await ctx.send(embed=emb)
        tim = random.randint(0, 5)
        await asyncio.sleep(tim)
        for i in reversed(range(0, 4)):
            emb = discord.Embed(title=f'{i}')
            await mess.edit(embed=emb)
            tim = random.randint(0, 1)
            await asyncio.sleep(tim)
        global message_id
        emb = discord.Embed(description='**!ЖМИ :cookie: НИЖЕ!**', color=discord.Colour.red())
        await mess.edit(embed=emb)
        emoji = '\N{cookie}'
        await mess.add_reaction(emoji)
        message_id = mess.id
        def check(reaction, user):
            return str(reaction.emoji) == emoji and user != self.bot.user
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=check)
            emb = discord.Embed(description=f'**Выиграл: __{user}__**', color=discord.Colour.gold())
            await mess.edit(embed=emb)
        except asyncio.TimeoutError:
            emb = discord.Embed(description=f'**Время вышло!\nНикто не поставил реакцию:cry:**', color=discord.Colour.blue())
            await mess.edit(embed=emb)


    @shootout.error
    async def shootout_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'shootout/перестрелка (Имя 1-ого игрока) (Имя 2-ого игрока) (Кол-во патронов 1-ого Игрока) (Кол-во патронов 2-ого Игрока)'
            await get_error(ctx, synt)
    @duel.error
    async def duel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'duel "Name 1" "Name 2"'
            await get_error(ctx, synt)



def setup(bot):
    bot.add_cog(_Minigames_(bot))