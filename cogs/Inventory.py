import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from datetime import datetime


class Inventory(commands.Cog):
    """Inventory commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["лот"], help = 'лот/lot <изменить/change> <item name> <new cost for lot>\nлот/lot <снять/del> <item name>\nлот/lot <выставить/put> <item name> <quantity> <cost>')
    async def lot(self, ctx, act, name, qu: int = None, cost: int = None):
        buyi = await get_data()
        emo = await get_ecoemoji(ctx)
        if (act == 'изменить' or act == 'change') and qu != None and cost == None:
            if not name in buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)]:
                emb = discord.Embed(description=f'Неккоректные данные')
                await ctx.send(embed=emb)
            if qu == None:
                emb = discord.Embed(description=f'Введите новую цену!')
                await ctx.send(embed=emb)
            else:
                buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['cost'] = qu
                emb = discord.Embed(description=f'Цена "{name}" была изменена\nТеперь она составляет **{buyi["servers"][str(ctx.guild.id)]["shop"]["item"][str(ctx.author.id)][name]["cost"]} {emo}**')
                await ctx.send(embed=emb)
        if (act == 'снять' or act == 'del') and qu == None and cost == None:
            if not name in buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)]:
                emb = discord.Embed(description=f'Неккоректные данные')
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'Слот "{name}" был снят')
                await ctx.send(embed=emb)
                if not str(ctx.author.id) in buyi['servers'][str(ctx.guild.id)]['inv']:
                    buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
                if not name in buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                    buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name] = {}
                    buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] = buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant']
                    del buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]
                else:
                    buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] += buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant']
                    del buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]
        if (act == 'выставить' or act == 'put') and cost != None and qu != None:
            if name in buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                if buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] < qu:
                    emb = discord.Embed(description=f'Вы пытаетесь выставить большее кол-во, чем имеете!')
                    await ctx.send(embed=emb)
                    exit
                if buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] > qu:
                    buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                    if not str(ctx.author.id) in buyi["servers"][str(ctx.guild.id)]["shop"]['item']:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)] = {}
                    if not name in buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)]:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name] = {}
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['cost'] = cost
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant'] = qu
                        emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за {cost} {emo}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
                    else:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['cost'] += cost
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant'] += qu
                        emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {emo}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                    exit
                if buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] == qu:
                    del buyi['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                    if not str(ctx.author.id) in buyi["servers"][str(ctx.guild.id)]["shop"]['item']:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)] = {}
                    if not name in buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)]:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name] = {}
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['cost'] = cost
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant'] = qu
                        emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за {cost} {emo}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
                    else:
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['cost'] += cost
                        buyi["servers"][str(ctx.guild.id)]["shop"]['item'][str(ctx.author.id)][name]['quant'] += qu
                        emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {emo}')
                        await ctx.send(embed=emb)
                        with open('cogs/data.json', 'w') as f:
                            json.dump(buyi, f)
                        exit
            else:
                emb = discord.Embed(description=f'Вы пытаетесь выставить предмет, которого нет у вас!')
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(buyi, f)
    @commands.command(aliases=["inv", "инвентарь"], help = 'inv <@member>')
    async def inventory(self, ctx, member: discord.Member = None):
        invs = await get_data()
        msg = ''
        c = 0
        if member == None or str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in invs['servers'][str(ctx.guild.id)]['inv']:
                invs['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
                with open('cogs/data.json', 'w') as f:
                    json.dump(invs, f)
            for inv in invs.copy()['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                msg += f'{invs["servers"][str(ctx.guild.id)]["inv"][str(ctx.author.id)][inv]["quanti"]}  —  {inv}\n'
                c += 1
            if c == 0:
                msg = f'пока нет вещей'
            emb = discord.Embed(title='Инвентарь', description=f'{msg}', timestamp=datetime.utcnow())
            emb.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        elif member != None and member != ctx.author.id:
            if not str(member.id) in invs['servers'][str(ctx.guild.id)]['inv']:
                invs['servers'][str(ctx.guild.id)]['inv'][str(member.id)] = {}
                with open('cogs/data.json', 'w') as f:
                    json.dump(invs, f)
            for inv in invs['servers'][str(ctx.guild.id)]['inv'][str(member.id)]:
                msg += f'{invs["servers"][str(ctx.guild.id)]["inv"][str(member.id)][inv]["quanti"]}  —  {inv}\n'
                c += 1
            if c == 0:
                msg = f'пока нет вещей'
            emb = discord.Embed(title='Инвентарь', description=f'{msg}', timestamp=datetime.utcnow())
            emb.set_author(name=f'{member}', icon_url=member.avatar_url)
            await ctx.send(embed=emb)



    @lot.error
    async def lot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'лот/lot <изменить/change> <item name> <new cost for lot>\nлот/lot <снять/del> <item name>\nлот/lot <выставить/put> <item name> <quantity> <cost>'
            await get_error(ctx, error, synt)

def setup(bot):
    bot.add_cog(Inventory(bot))