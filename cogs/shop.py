import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *


class _Shop_(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["магазин"])
    async def shop(self, ctx, name=None):
        with open('cogs/data.json', 'r') as f:
            shop = json.load(f)
        if name == None:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop ролей/role**" либо "**-магазин/shop предметов/item**"')
            await ctx.send(embed=emb)
        elif name == 'ролей' or name == 'роль' or name == 'role' or name == 'roles':
            emb = discord.Embed(title="Магазин Ролей")
            for role in shop['shop']['Role']:
                emb.add_field(name=f'Цена: {shop["shop"]["Role"][role]["Cost"]}', value=f'Роль: <@&{role}>\nКоличество: {shop["shop"]["Role"][role]["Quant"]}', inline=False)
            await ctx.send(embed=emb)
        elif name == 'предметов' or name == 'предмет' or name == 'item' or name == 'items':
            emb = discord.Embed(title="Магазин Предметов")
            for user in shop['shop']['item']:
                for item in shop['shop']['item'][str(user)]:
                    emb.add_field(name=f'Товар: {item}\n', value=f'**Цена: {shop["shop"]["item"][str(user)][item]["cost"]}** {self.bot.eco_emoji}\nКоличество: {shop["shop"]["item"][str(user)][item]["quant"]}\nВыставил: <@{user}>', inline=False)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop ролей/role**" либо "**-магазин/shop предметов/item**"')
            await ctx.send(embed=emb)
    @commands.command(aliases=["buy-role", "купить-роль"])
    async def buyrole(self, ctx, role: discord.Role):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        if not str(role.id) in money['shop']['Role']:
            await ctx.send('Такой роли не выставленно в магазине ролей')
        else:
            if str(role.id) in money['shop']['Role']:
                if money['shop']['Role'][str(role.id)]['Cost'] <= money['money'][str(ctx.author.id)]['Money']:
                    if not role in ctx.author.roles:
                        buy = discord.utils.get(self, ctx.guild.roles, id=int(role.id))
                        await ctx.author.add_roles(buy)
                        money['shop']['Role'][str(role.id)]['Quant'] -= 1
                        money['money'][str(ctx.author.id)]['Money'] -= money['shop']['Role'][str(role.id)]['Cost']
                        if money['shop']['Role'][str(role.id)]['Quant'] == 0:
                            del money['shop']['Role'][str(role.id)]
                            await ctx.send('Вы купили последний слот!')
                        else:
                            await ctx.send('Вы купили роль!')
                    else:
                        await ctx.send('У вас уже есть эта роль!')
                else:
                    await ctx.send('У вас недостаточно денег!')
        with open('cogs/data.json', 'w') as f:
            json.dump(money, f)
    @commands.command(aliases=["buy-item", "купить-предмет"])
    async def buyitem(self, ctx, item, member: discord.Member=None):
        with open('cogs/data.json', 'r') as f:
            buyi = json.load(f)
        if not str(ctx.author.id) in buyi['money']:
            buyi['money'][str(ctx.author.id)] = {}
            buyi['money'][str(ctx.author.id)]['Money'] = 0
            buyi['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
        if not str(member.id) in buyi['money']:
            buyi['money'][str(member.id)] = {}
            buyi['money'][str(member.id)]['Money'] = 0
            buyi['money'][str(member.id)]['Name'] = str(member)
        if not str(member.id) in buyi['shop']['item']:
            emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
            await ctx.send(embed=emb)
        elif not str(item) in buyi['shop']['item'][str(member.id)]:
            emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
            await ctx.send(embed=emb)
        else:
            if buyi['shop']['item'][str(member.id)][item]['cost'] <= buyi['money'][str(ctx.author.id)]['Money']:
                buyi['money'][str(ctx.author.id)]['Money'] -= buyi['shop']['item'][str(member.id)][item]['cost']
                buyi['money'][str(member.id)]['Money'] += buyi['shop']['item'][str(member.id)][item]['cost']
                if not str(ctx.author.id) in buyi['inv']:
                    buyi['inv'][str(ctx.author.id)] = {}
                buyi['inv'][str(ctx.author.id)][item] = {}
                buyi['inv'][str(ctx.author.id)][item]['quanti'] = buyi['shop']['item'][str(member.id)][item]['quant']
                emb = discord.Embed(description=f'Вы купили "{item}" в количестве {buyi["inv"][str(ctx.author.id)][item]["quanti"]} за {buyi["shop"]["item"][str(member.id)][item]["cost"]} {self.bot.eco_emoji}')
                del buyi['shop']['item'][str(member.id)][item]
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(buyi, f)
    @commands.command(aliases=["передать", "transfer", "trans"])
    async def give(self, ctx, what, member: discord.Member, arg: int, name=None):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        if what == 'деньги' and name == None:
            if not str(member.id) in money['money']:
                money['money'][str(member.id)] = {}
                money['money'][str(member.id)]['Money'] = 0
            if money['money'][str(ctx.author.id)]['Money'] >= arg:
                emb = discord.Embed(description=f'**{ctx.author}** подарил **{member}** **{arg}** {self.bot.eco_emoji}')
                money['money'][str(ctx.author.id)]['Money'] -= arg
                money['money'][str(member.id)]['Money'] += arg
                await ctx.send(embed=emb)
            else:
                await ctx.send('У вас недостаточно денег')
        elif what == 'предмет' and name != None:
            if not str(member.id) in money['inv']:
                money['inv'][str(member.id)] = {}
            if name in money['inv'][str(ctx.author.id)]:
                if arg > money['inv'][str(ctx.author.id)][name]['quanti']:
                    emb = discord.Embed(description=f'Вы не можете передать больше, чем имеете!')
                    await ctx.send(embed=emb)
                else:
                    if arg < money['inv'][str(ctx.author.id)][name]['quanti']:
                        money['inv'][str(ctx.author.id)][name]['quanti'] -= arg
                    if arg == money['inv'][str(ctx.author.id)][name]['quanti']:
                        del money['inv'][str(ctx.author.id)][name]
                    if name in money['inv'][str(member.id)]:
                        money['inv'][str(member.id)][name]['quanti'] += arg
                        emb = discord.Embed(description=f'Вы передали {member} {arg} единиц "{name}"')
                        await ctx.send(embed=emb)
                    else:
                        money['inv'][str(member.id)][name] = {}
                        money['inv'][str(member.id)][name]['quanti'] = arg
                        emb = discord.Embed(description=f'Вы передали {member} {arg} единиц "{name}"')
                        await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У вас нет этого предмета!')
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Введены неккорентые данные!\nДля помощи напишите "**-помощь передать**"')
            await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(money, f)


    @buyrole.error
    async def buyrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'buy-role/buyrole <@Role>'
            await get_error(ctx, error, synt)
    @buyitem.error
    async def buyitem_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'buy-item/buyitem <item-name> <@member>'
            await get_error(ctx, error, synt)
    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'give/trans <item/money> <@member> <qunatity> (If item: name-item)'
            await get_error(ctx, error, synt)

def setup(bot):
    bot.add_cog(_Shop_(bot))