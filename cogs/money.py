import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio



class _Money(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wages"])
    async def зп(self, ctx):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        if not str(ctx.author.id) in money['money']:
            money['money'][str(ctx.author.id)] = {}
            money['money'][str(ctx.author.id)]['Money'] = 0
            money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
        if not str(ctx.author.id) in queue:
            emb = discord.Embed(
                description=f'**{ctx.author}** Вы получили свои 150 {self.bot.eco_emoji}\nСледующее получение будет доступно только через 2 минуты')
            await ctx.send(embed=emb)
            money['money'][str(ctx.author.id)]['Money'] += 150
            queue.append(str(ctx.author.id))
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
            await asyncio.sleep(120)
            queue.remove(str(ctx.author.id))
        if str(ctx.author.id) in queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed=emb)
    @commands.command(aliases=["balance", "bal"])
    async def баланс(self, ctx, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            balance = json.load(f)
        if not str(ctx.author.id) in balance['money']:
            balance['money'][str(ctx.author.id)] = {}
            balance['money'][str(ctx.author.id)]['Money'] = 0
            balance['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
            with open('cogs/data.json', 'w') as f:
                json.dump(balance, f)
        if member == None:
            emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        elif str(member.id) == str(ctx.author.id):
            emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        else:
            if not str(member.id) in balance['money']:
                balance['money'][str(member.id)] = {}
                balance['money'][str(member.id)]['Money'] = 0
                balance['money'][str(member.id)]['Name'] = str(member)
            emb = discord.Embed(description=f'У **{member}** на счету {balance["money"][str(member.id)]["Money"]} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
            emb.set_author(name=member.name, icon_url=member.avatar_url)
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(_Money(bot))