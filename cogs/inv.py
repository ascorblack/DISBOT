import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *


class _Inventory_(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["лот"])
    async def lot(self, ctx, act, name, qu: int = None, cost: int = None):
        with open('cogs/data.json', 'r') as f:
            buyi = json.load(f)
        if (act == 'изменить' or act == 'change') and qu != None and cost == None:
            if not name in buyi['shop']['item'][str(ctx.author.id)]:
                emb = discord.Embed(description=f'Неккоректные данные')
                await ctx.send(embed=emb)
            if qu == None:
                emb = discord.Embed(description=f'Введите новую цену!')
                await ctx.send(embed=emb)
            else:
                buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = qu
                emb = discord.Embed(description=f'Цена "{name}" была изменена\nТеперь она составляет **{buyi["shop"]["item"][str(ctx.author.id)][name]["cost"]} {self.bot.eco_emoji}**')
                await ctx.send(embed=emb)
        if (act == 'снять' or act == 'del') and qu == None and cost == None:
            if not name in buyi['shop']['item'][str(ctx.author.id)]:
                emb = discord.Embed(description=f'Неккоректные данные')
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'Слот "{name}" был снят')
                await ctx.send(embed=emb)
                if not str(ctx.author.id) in buyi['inv']:
                    buyi['inv'][str(ctx.author.id)] = {}
                if not name in buyi['inv'][str(ctx.author.id)]:
                    buyi['inv'][str(ctx.author.id)][name] = {}
                    buyi['inv'][str(ctx.author.id)][name]['quanti'] = buyi['shop']['item'][str(ctx.author.id)][name]['quant']
                    del buyi['shop']['item'][str(ctx.author.id)][name]
                else:
                    buyi['inv'][str(ctx.author.id)][name]['quanti'] += buyi['shop']['item'][str(ctx.author.id)][name]['quant']
                    del buyi['shop']['item'][str(ctx.author.id)][name]
        if (act == 'выставить' or act == 'put') and cost != None and qu != None:
            if name in buyi['inv'][str(ctx.author.id)]:
                if buyi['inv'][str(ctx.author.id)][name]['quanti'] < qu:
                    emb = discord.Embed(description=f'Вы пытаетесь выставить большее кол-во, чем имеете!')
                    await ctx.send(embed=emb)
                    exit
                if buyi['inv'][str(ctx.author.id)][name]['quanti'] > qu:
                    buyi['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                    if not str(ctx.author.id) in buyi['shop']['item']:
                        buyi['shop']['item'][str(ctx.author.id)] = {}
                    if not name in buyi['shop']['item'][str(ctx.author.id)]:
                        buyi['shop']['item'][str(ctx.author.id)][name] = {}
                        buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                        buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                        emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} {self.bot.eco_emoji}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
                    else:
                        buyi['shop']['item'][str(ctx.author.id)][name]['cost'] += cost
                        buyi['shop']['item'][str(ctx.author.id)][name]['quant'] += qu
                        emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {self.bot.eco_emoji}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                    exit
                if buyi['inv'][str(ctx.author.id)][name]['quanti'] == qu:
                    del buyi['inv'][str(ctx.author.id)][name]
                    if not str(ctx.author.id) in buyi['shop']['item']:
                        buyi['shop']['item'][str(ctx.author.id)] = {}
                    if not name in buyi['shop']['item'][str(ctx.author.id)]:
                        buyi['shop']['item'][str(ctx.author.id)][name] = {}
                        buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                        buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                        emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} {self.bot.eco_emoji}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
                    else:
                        buyi['shop']['item'][str(ctx.author.id)][name]['cost'] += cost
                        buyi['shop']['item'][str(ctx.author.id)][name]['quant'] += qu
                        emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {self.bot.eco_emoji}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
            else:
                emb = discord.Embed(description=f'Вы пытаетесь выставить предмет, которого нет у вас!')
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(buyi, f)
    @commands.command(aliases=["inv", "инвентарь"])
    async def inventory(self, ctx, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            invs = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in invs['inv']:
                invs['inv'][str(ctx.author.id)] = {}
            emb = discord.Embed(title='Ваши предметы')
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            for inv in invs.copy()['inv'][str(ctx.author.id)]:
                emb.add_field(name=f'Предмет: {inv}', value=f'Количество: {invs["inv"][str(ctx.author.id)][inv]["quanti"]}', inline=False)
            await ctx.send(embed=emb)
        elif member != None and member != ctx.author.id:
            if not str(member.id) in invs['inv']:
                invs['inv'][str(member.id)] = {}
            emb = discord.Embed(title=f'Его предметы')
            emb.set_author(name=f'Инвентарь {member.name}', icon_url=member.avatar_url)
            for inv in invs['inv'][str(member.id)]:
                emb.add_field(name=f'Предмет: {inv}', value=f'Количество: {invs["inv"][str(member.id)][inv]["quanti"]}', inline=False)
            await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(invs, f)


    @lot.error
    async def lot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'лот/lot <изменить/change> <item name> <new cost for lot>\nлот/lot <снять/del> <item name>\nлот/lot <выставить/put> <item name> <cost> <quantity>'
            await get_error(ctx, error, synt)

def setup(bot):
    bot.add_cog(_Inventory_(bot))