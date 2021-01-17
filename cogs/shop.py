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
        emo = await get_ecoemoji(ctx)
        if name == None:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop ролей/role**" либо "**-магазин/shop предметов/item**"')
            await ctx.send(embed=emb)
        elif name == 'ролей' or name == 'роль' or name == 'role' or name == 'roles':
            emb = discord.Embed(title="Магазин Ролей")
            for role in shop["servers"][str(ctx.guild.id)]['shop']['Role']:
                emb.add_field(name=f'Цена: {shop["servers"][str(ctx.guild.id)]["shop"]["Role"][role]["Cost"]}', value=f'Роль: <@&{role}>\nКоличество: {shop["servers"][str(ctx.guild.id)]["shop"]["Role"][role]["Quant"]}', inline=False)
            await ctx.send(embed=emb)
        elif name == 'предметов' or name == 'предмет' or name == 'item' or name == 'items':
            emb = discord.Embed(title="Магазин Предметов")
            for user in shop["servers"][str(ctx.guild.id)]['shop']['item']:
                for item in shop["servers"][str(ctx.guild.id)]['shop']['item'][str(user)]:
                    emb.add_field(name=f'Товар: {item}\n', value=f'**Цена: {shop["servers"][str(ctx.guild.id)]["shop"]["item"][str(user)][item]["cost"]}** {emo}\nКоличество: {shop["servers"][str(ctx.guild.id)]["shop"]["item"][str(user)][item]["quant"]}\nВыставил: <@{user}>', inline=False)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин/shop ролей/role**" либо "**-магазин/shop предметов/item**"')
            await ctx.send(embed=emb)
    @commands.command(aliases=["buy-role", "купить-роль"])
    async def buyrole(self, ctx, role: discord.Role):
        with open('cogs/data.json', 'r') as f:
            money = json.load(f)
        if not str(role.id) in money["servers"][str(ctx.guild.id)]['shop']['Role']:
            emb = discord.Embed(description=f'Роль **{role}** не выставлена в магазине!')
            await ctx.send(embed=emb)
        else:
            if str(role.id) in money["servers"][str(ctx.guild.id)]['shop']['Role']:
                if money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Cost'] <= money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money']:
                    if not role in ctx.author.roles:
                        buy = discord.utils.get(ctx.guild.roles, id=int(role.id))
                        await ctx.author.add_roles(buy)
                        money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Quant'] -= 1
                        money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] -= money["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Cost']
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
    @commands.command(aliases=["buy-item", "купить-предмет"])
    async def buyitem(self, ctx, item, member: discord.Member=None):
        with open('cogs/data.json', 'r') as f:
            buyi = json.load(f)
        emo = await get_ecoemoji(ctx)
        if not str(ctx.author.id) in buyi['servers'][str(ctx.guild.id)]['money']:
            buyi['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)] = {}
            buyi['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] = 0
            buyi['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
        if not str(member.id) in buyi['servers'][str(ctx.guild.id)]['money']:
            buyi['servers'][str(ctx.guild.id)]['money'][str(member.id)] = {}
            buyi['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] = 0
            buyi['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Name'] = str(member)
        if not str(member.id) in buyi["servers"][str(ctx.guild.id)]['shop']['item']:
            emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
            await ctx.send(embed=emb)
        elif not str(item) in bui["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)]:
            emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
            await ctx.send(embed=emb)
        else:
            if buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost'] <= buyi['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money']:
                buyi['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] -= buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost']
                buyi['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] += buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['cost']
                if not str(ctx.author.id) in bui["servers"][str(ctx.guild.id)]['inv']:
                    buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
                buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][item] = {}
                buyi["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][item]['quanti'] = buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]['quant']
                emb = discord.Embed(description=f'Вы купили "{item}" в количестве {buyi["servers"][str(ctx.guild.id)]["inv"][str(ctx.author.id)][item]["quanti"]} за {buyi["servers"][str(ctx.guild.id)]["shop"]["item"][str(member.id)][item]["cost"]} {emo}')
                del buyi["servers"][str(ctx.guild.id)]['shop']['item'][str(member.id)][item]
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(buyi, f)
    @commands.command(aliases=["передать", "transfer", "trans"])
    async def give(self, ctx, what, member: discord.Member, arg: int, name=None):
        money = await get_data()
        emo = await get_ecoemoji(ctx)
        if (what == 'деньги' or what == 'money') and name == None:
            if not str(member.id) in money['servers'][str(ctx.guild.id)]['money']:
                money['servers'][str(ctx.guild.id)]['money'][str(member.id)] = {}
                money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] = 0
            if money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] >= arg:
                emb = discord.Embed(description=f'**{ctx.author}** отправил **{member}** — **{arg}** {emo}')
                money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] -= arg
                money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] += arg
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У вас недостаточно денег')
                await ctx.send(embed=emb)
        elif (what == 'предмет' or what == 'item') and name != None:
            if not str(member.id) in money["servers"][str(ctx.guild.id)]['inv']:
                money["servers"][str(ctx.guild.id)]['inv'][str(member.id)] = {}
            if name in money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                if arg > money["servers"][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti']:
                    emb = discord.Embed(description=f'Вы не можете передать больше, чем имеете!')
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
        else:
            emb = discord.Embed(description=f'Введены неккорентые данные!\nДля помощи напишите "**-помощь передать**"')
            await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(money, f)


    @buyrole.error
    async def buyrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'buy-role/buyrole <@Role>'
            await get_error(ctx, synt)
    @buyitem.error
    async def buyitem_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'buy-item/buyitem <item-name> <@member>'
            await get_error(ctx, synt)
    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'give/trans <item/money> <@member> <qunatity> (If item: name-item)'
            await get_error(ctx, synt)

def setup(bot):
    bot.add_cog(_Shop_(bot))