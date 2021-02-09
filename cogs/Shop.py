import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *


class Shop(commands.Cog):
    """Shop commands"""
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases=["магазин"], help = 'shop role/item')
    async def shop(self, ctx, name=None):
        with open('cogs/data.json', 'r') as f:
            shop = json.load(f)
        msg = ''
        emo = await get_ecoemoji(ctx)
        if name == None:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop <ролей/role>**" либо "**-магазин/shop <предметов/item>**"', color = discord.Colour.dark_green())
            await ctx.send(embed=emb)
        elif name == 'ролей' or name == 'роль' or name == 'role' or name == 'roles':
            for role in shop["servers"][str(ctx.guild.id)]['shop']['Role']:
                msg += f'__Роль: <@&{role}>__\nЦена: **{shop["servers"][str(ctx.guild.id)]["shop"]["Role"][role]["Cost"]}** {emo}\nКоличество: {shop["servers"][str(ctx.guild.id)]["shop"]["Role"][role]["Quant"]}\n\n'
            emb = discord.Embed(title="Магазин Ролей", description=msg, color = discord.Colour.dark_magenta())
            await ctx.send(embed=emb)
        elif name == 'предметов' or name == 'предмет' or name == 'item' or name == 'items':
            for user in shop["servers"][str(ctx.guild.id)]['shop']['item']:
                for item in shop["servers"][str(ctx.guild.id)]['shop']['item'][str(user)]:
                    msg += f'__Товар: {item}__\nЦена: **{shop["servers"][str(ctx.guild.id)]["shop"]["item"][str(user)][item]["cost"]}** {emo}\nКоличество: {shop["servers"][str(ctx.guild.id)]["shop"]["item"][str(user)][item]["quant"]}\nВыставил: <@{user}>\n\n'
            emb = discord.Embed(title="Магазин Предметов", description=msg, color = discord.Colour.dark_magenta())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop ролей/role**" либо "**-магазин/shop предметов/item**"')
            await ctx.send(embed=emb)
    @commands.command(aliases=["buy-role", "купить-роль"], help = 'buy-role/buyrole <@Role>')
    async def buyrole(self, ctx, role: discord.Role):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        member = ctx.author
        bal = await get_money(ctx, member)
        if not str(role.id) in money["servers"][str(ctx.guild.id)]['shop']['Role']:
            emb = discord.Embed(description=f'Роль **{role}** не выставлена в магазине!')
            await ctx.send(embed=emb)
        else:
            if str(role.id) in money["servers"][str(ctx.guild.id)]['shop']['Role']:
                if money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Cost'] <= bal:
                    if not role in ctx.author.roles:
                        buy = discord.utils.get(ctx.guild.roles, id=int(role.id))
                        await ctx.author.add_roles(buy)
                        money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Quant'] -= 1
                        await up_money(ctx, member, co = -money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Cost'])
                        db.commit()
                        if money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Quant'] == 0:
                            del money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]
                            emb = discord.Embed(description=f'Вы купили последний слот!')
                            await ctx.send(embed=emb)
                        else:
                            emb = discord.Embed(description=f'Вы купили роль **{role}**!')
                            await ctx.send(embed=emb)
                    else:
                        emb = discord.Embed(description=f'У вас уже есть роль **{role}**!')
                        await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(description=f'У вас недостаточно денег для покупки!')
                    await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(money, f)
    @commands.command(aliases=["buy-item", "купить-предмет"], help = 'buy-item/buyitem <item-name> <@member>')
    async def buyitem(self, ctx, item, member: discord.Member=None):
        with open('cogs/data.json', 'r') as f:
            buyi = json.load(f)
        emo = await get_ecoemoji(ctx)
        if not str(member.id) in buyi["servers"][str(ctx.guild.id)]['shop']['item']:
            emb = discord.Embed(description=f'Пользователь {member} ничего не продаёт!')
            await ctx.send(embed=emb)
        elif not str(item) in buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)]:
            emb = discord.Embed(description=f'У {member} не выставленно предмета {item}!')
            await ctx.send(embed=emb)
        else:
            bal = await get_money(ctx, member = ctx.author)
            if buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost'] <= bal:
                await up_money(ctx, member, co = +buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost'])
                db.commit()
                member = ctx.author
                await up_money(ctx, member, co = -buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost'])
                db.commit()
                if not str(ctx.author.id) in buyi["servers"][str(ctx.guild.id)]['inv']:
                    buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
                buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][item] = {}
                buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][item]['quanti'] = buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['quant']
                emb = discord.Embed(description=f'Вы купили "{item}" в количестве {buyi["servers"][str(ctx.guild.id)]["inv"][str(ctx.author.id)][item]["quanti"]} за {buyi["servers"][str(ctx.guild.id)]["shop"]["item"][str(member.id)][item]["cost"]} {emo}')
                del buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У вас недостаточно {emo}!')
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(buyi, f)
    @commands.command(aliases=["give"], help = 'give/trans <@member> <item-name> <quantity>')
    async def transfer(self, ctx, member: discord.Member, name = None, arg = 0):
        money = await get_data()
        if arg <= 0:
            emb = discord.Embed(description=f'Вы не можете передать отрицательное/нулевое количество!')
            await ctx.send(embed=emb)
            exit
        if not str(member.id) in money["servers"][str(ctx.guild.id)]['inv']:
            money["servers"][str(ctx.guild.id)]['inv'][str(member.id)] = {}
        if name in money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
            if arg > money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti']:
                emb = discord.Embed(description=f'Вы не можете передать больше {name}, чем имеете!')
                await ctx.send(embed=emb)
            else:
                if arg < money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti']:
                    money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] -= arg
                if arg == money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti']:
                    del money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                if name in money["servers"][str(ctx.guild.id)]['inv'][str(member.id)]:
                    money["servers"][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti'] += arg
                    emb = discord.Embed(description=f'**{ctx.author}** передал **{member}** {arg} единиц __"{name}"__')
                    await ctx.send(embed=emb)
                else:
                    money["servers"][str(ctx.guild.id)]['inv'][str(member.id)][name] = {}
                    money["servers"][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti'] = arg
                    emb = discord.Embed(description=f'**{ctx.author}** передал **{member}** {arg} единиц __"{name}"__')
                    await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'У вас нет этого предмета!')
            await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(money, f)
    @commands.command(help = 'pay <@member> <quantity money>')
    async def pay(self, ctx, member: discord.Member, qu: int):
        balau = await get_money(ctx, member = ctx.author)
        emo = await get_ecoemoji(ctx)
        if qu <= 0:
            emb = discord.Embed(description=f'Вы не можете передать отрицательное/нулевое количество {emo}')
            await ctx.send(embed=emb)
        else:
            if balau >= qu:
                await up_money(ctx, member, co = +qu)
                db.commit()
                await up_money(ctx, member = ctx.author, co = -qu)
                db.commit()
                emb = discord.Embed(description=f'{ctx.author} передал {member} {qu} {emo}')
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У вас недостаточно {emo} для такой транзакции!')
                await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Shop(bot))