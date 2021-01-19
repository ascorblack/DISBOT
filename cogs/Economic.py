import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import * 


class Economic(commands.Cog):
    """Economic commands"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["зп"], help = 'wages')
    async def wages(self, ctx):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        emo = await get_ecoemoji(ctx)
        if not str(ctx.author.id) in money['servers'][str(ctx.guild.id)]['money']:
            money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)] = {}
            money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] = 0
            money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
        if not str(ctx.author.id) in self.bot.queue:
            emb = discord.Embed(
                description=f'**{ctx.author}** Вы получили свои 150 {emo}\nСледующее получение будет доступно только через 2 минуты')
            await ctx.send(embed=emb)
            money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] += 150
            self.bot.queue.append(str(ctx.author.id))
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
            await asyncio.sleep(120)
            self.bot.queue.remove(str(ctx.author.id))
        if str(ctx.author.id) in self.bot.queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed=emb)
    @commands.command(aliases=["баланс", "bal"], help = '-balance <@member>')
    async def balance(self, ctx, member: discord.Member = None):
        balance = await get_data()
        emo = await get_ecoemoji(ctx)
        if not str(ctx.author.id) in balance['servers'][str(ctx.guild.id)]['money']:
            balance['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)] = {}
            balance['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] = 0
            balance['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
            with open('cogs/data.json', 'w') as f:
                json.dump(balance, f)
        if member == None:
            emb = discord.Embed(description=f'У вас на счету {balance["servers"][str(ctx.guild.id)]["money"][str(ctx.author.id)]["Money"]} {emo}', color=discord.Colour.dark_green())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        elif str(member.id) == str(ctx.author.id):
            emb = discord.Embed(description=f'У вас на счету {balance["servers"][str(ctx.guild.id)]["money"][str(ctx.author.id)]["Money"]} {emo}', color=discord.Colour.dark_green())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        else:
            if not str(member.id) in balance['servers'][str(ctx.guild.id)]['money']:
                balance['servers'][str(ctx.guild.id)]['money'][str(member.id)] = {}
                balance['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] = 0
                balance['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Name'] = str(member)
            emb = discord.Embed(description=f'У **{member}** на счету {balance["servers"][str(ctx.guild.id)]["money"][str(member.id)]["Money"]} {emo}', color=discord.Colour.dark_green())
            emb.set_author(name=member.name, icon_url=member.avatar_url)
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Economic(bot))