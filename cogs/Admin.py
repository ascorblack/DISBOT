import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *


class Admin(commands.Cog):
    """Commands for Administrators and Owners only"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop', aliases=["стоп"], pass_context=True)
    @commands.is_owner()
    async def stop(self, ctx):
            await ctx.send('Ну ББ, KEKW')
            await self.bot.logout()
    @commands.command(aliases=["чистка"], help = 'clear <count>')
    @has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        emb = discord.Embed(color=discord.Colour.dark_grey(), description='Было отчищенно ' + str(amount) + ' сообщений!')
        await ctx.send(embed=emb)
    @commands.command(aliases=["spam"], help = 'шнюк/nuke <quanti> <text>')
    @has_permissions(administrator=True)
    async def шнюк(self, ctx, k, *, text):
        mess = await get_last_mess(ctx, member = None)
        await mess.delete()
        i = 0
        while i < int(k):
            await ctx.send(text)
            i += 1
    @commands.command(aliases=["нюк"], hidden = True)
    @commands.is_owner()
    async def nuke(self, ctx):
        await ctx.send('https://tenor.com/view/destory-eexplode-nuke-gif-6073338')
    @commands.command(help = 'say <text>')
    @commands.is_owner()
    async def say(self, ctx, *, text):
        if not text == None:
            mess = await last_mess(ctx, member = None)
            await mess.delete()
            await ctx.send(text)
    @commands.command(aliases=["добавить-предмет", "add-item"], help = 'add-item/additem <name> <quanti> <@member>')
    @has_permissions(administrator=True)
    async def additem(self, ctx, name, qu: int, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            add = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in add['servers'][str(ctx.guild.id)]['inv']:
                add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
            if not name in add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name] = {}
                add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] = qu
                emb = discord.Embed(description=f':white_check_mark: Вы добавили предмет "{name}" в количестве {str(qu)}')
                await ctx.send(embed=emb)
                if add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
            else:
                add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] += qu
                if qu < 0:
                    emb = discord.Embed(description=f':white_check_mark: Вы уменьшили количество предмета "{name}" на {str(-qu)}')
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(description=f':white_check_mark: Вы увеличили количество предмета "{name}" на {str(qu)}')
                    await ctx.send(embed=emb)
                if add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
        else:
            if not str(member.id) in add['servers'][str(ctx.guild.id)]['inv']:
                add['servers'][str(ctx.guild.id)]['inv'][str(member.id)] = {}
            if not name in add['servers'][str(ctx.guild.id)]['inv'][str(member.id)]:
                add['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name] = {}
                add['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti'] = qu
                with open('cogs/data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы добавили **{member}** предмет "{name}", теперь у него его {add["servers"][str(ctx.guild.id)]["inv"][str(member.id)][name]["quanti"]} штук')
                await ctx.send(embed=emb)
            else:
                add['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti'] += qu
                with open('cogs/data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы прибавили **{member}** {qu} предмета "{name}"\nТеперь у него его {add["servers"][str(ctx.guild.id)]["inv"][str(member.id)][name]["quanti"]} штук')
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(add, f)
    @commands.command(aliases=["удалить-предмет", "del-item"], help = 'del-item/delitem <name> <quanti> <@member>')
    @has_permissions(administrator=True)
    async def delitem(self, ctx, name, qu=754325616, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            rem = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not name in rem['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)]:
                await ctx.send(':no_entry_sign: у вас нет такого предмета в инвентаре!')
                exit
            else:
                if qu <= 0:
                    await ctx.send(':no_entry_sign: Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu == 754325616:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                elif qu >= rem['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]
                else:
                    rem['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(qu)} предмета "{name}"')
                    await ctx.send(embed=emb)
        elif member != str(ctx.author.id):
            if not name in rem['servers'][str(ctx.guild.id)]['inv'][str(member.id)]:
                emb = discord.Embed(description=f'У {member.mention} нет такого предмета в инвентаре')
                await ctx.send(embed=emb)
                exit
            else:
                if qu <= 0:
                    await ctx.send('Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu >= rem['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(rem["servers"][str(ctx.guild.id)]["inv"][str(member.id)][name]["quanti"])} "{name}"')
                    await ctx.send(embed=emb)
                    del rem['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name]
                else:
                    rem['servers'][str(ctx.guild.id)]['inv'][str(member.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(qu)} "{name}"')
                    await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(rem, f)
    @commands.command(aliases=["выставить-роль", "shop-add-role", "sar"], help = 'shop-add-role/sar/shopaddrole <@ROLE> <count> <quanti>')
    @has_permissions(administrator=True)
    async def shopaddrole(self, ctx, role: discord.Role, cost: int, quant=1):
        if quant <= 0:
            emb = discord.Embed(description=f':no_entry_sign: Невозможно выставить отрицательное/нулеовое кол-во слотов!')
            await ctx.send(embed=emb)
            pass
        else:
            with open('cogs/data.json', 'r') as f:
                add = json.load(f)
            if str(role.id) in add["servers"][str(ctx.guild.id)]["shop"]:
                emb = discord.Embed(description=f":no_entry_sign: **{role}** уже есть в магазине")
                await ctx.send(embed=emb)
            if not str(role.id) in add["servers"][str(ctx.guild.id)]["shop"]:
                add["servers"][str(ctx.guild.id)]["shop"]['Role'][str(role.id)] = {}
                add["servers"][str(ctx.guild.id)]["shop"]['Role'][str(role.id)]['Cost'] = cost
                add["servers"][str(ctx.guild.id)]["shop"]['Role'][str(role.id)]['Quant'] = quant
                emb = discord.Embed(description=f':white_check_mark: Роль **{role}** добавлена в магазин')
                await ctx.send(embed=emb)
            with open('cogs/data.json', 'w') as f:
                json.dump(add, f)
    @commands.command(aliases=["удалить-роль", "shop-del-role", "sdr"], help = 'shop-del-role/sdr/shopdelrole <@ROLE> <count>')
    @has_permissions(administrator=True)
    async def shopdelrole(self, ctx, role: discord.Role, quant=None):
        if quant == None:
            with open('cogs/data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove["servers"][str(ctx.guild.id)]['shop']['Role']:
                await ctx.send(":no_entry_sign: Этой роли нет в магазине")
            if str(role.id) in remove["servers"][str(ctx.guild.id)]['shop']['Role']:
                emb = discord.Embed(description=f':white_check_mark: Роль **{role}** удалена из магазина')
                await ctx.send(embed=emb)
                del remove["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]
            with open('cogs/data.json', 'w') as f:
                json.dump(remove, f)
        else:
            with open('cogs/data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove["servers"][str(ctx.guild.id)]['shop']['Role']:
                emb = discord.Embed(description=f":no_entry_sign: Роли **{role}** нет в магазине")
                await ctx.send(embed=emb)
            if int(quant) > remove["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Quant']:
                with open('cogs/data.json', 'r') as f:
                    remove = json.load(f)
                if str(role.id) in remove["servers"][str(ctx.guild.id)]['shop']['Role']:
                    emb = discord.Embed(description=f':white_check_mark: Роль **{role}** удалена из магазина')
                    await ctx.send(embed=emb)
                    del remove["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]
                with open('cogs/data.json', 'w') as f:
                    json.dump(remove, f)
            else:
                if str(role.id) in remove["servers"][str(ctx.guild.id)]['shop']['Role']:
                    remove["servers"][str(ctx.guild.id)]['shop']['Role'][str(role.id)]['Quant'] -= int(quant)
                    emb = discord.Embed(description=f':white_check_mark:  {str(quant)} выставленных слотов роли было удалено из магазина')
                    await ctx.send(embed=emb)
                with open('cogs/data.json', 'w') as f:
                    json.dump(remove, f)
    @commands.command(aliases=["добавить-деньги", "add-money"], help = 'addmoney/add-money <quanti> <@member>')
    @has_permissions(administrator=True)
    async def addmoney(self, ctx, qu: int, member: discord.Member = None):
        emo = await get_ecoemoji(ctx)
        if qu > 0:
            with open('cogs/data.json', 'r') as f:
                money = json.load(f)
            if member == None or str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money['servers'][str(ctx.guild.id)]['money']:
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)] = {}
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] = 0
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
                if str(ctx.author.id) in money['servers'][str(ctx.guild.id)]['money']:
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на свой счёт {qu} {emo}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money["servers"][str(ctx.guild.id)]["money"]:
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)] = {}
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] = 0
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Name'] = str(member)
                if str(member.id) in money["servers"][str(ctx.guild.id)]["money"]:
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на счёт **{member}** {qu} {emo}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете добавить отрицательно/нулевое количество {emo}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["удалить-деньги", "del-money"], help = 'delmoney/del-money <quanti> <@member>')
    @has_permissions(administrator=True)
    async def delmoney(self, ctx, qu: int, member: discord.Member = None):
        emo = await get_ecoemoji(ctx)
        if qu > 0:
            with open('cogs/data.json', 'r') as f:
                money = json.load(f)
            if member == None or str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money["servers"][str(ctx.guild.id)]["money"]:
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)] = {}
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] = 0
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
                if str(ctx.author.id) in money['servers'][str(ctx.guild.id)]['money']:
                    money['servers'][str(ctx.guild.id)]['money'][str(ctx.author.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со своего счёта {qu} {emo}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money['servers'][str(ctx.guild.id)]['money']:
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)] = {}
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] = 0
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Name'] = str(member)
                if str(member.id) in money['servers'][str(ctx.guild.id)]['money']:
                    money['servers'][str(ctx.guild.id)]['money'][str(member.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со счёта **{member}** {qu} {emo}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете удалить отрицательно/нулевое количество {emo}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["бан"], help = 'ban <@member> <reason>')
    @has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member = None, reason = None):
        mess = str(member)
        if member == None or str(member.id) == str(ctx.author.id):
            emb = discord.Embed(description=f'<@{ctx.author.id}> Дурак совсем?')
            await ctx.send(embed=emb)
            exit
        if reason == None:
            reason = "по рофлу"
        emb = discord.Embed(description=f'Вы забанили **{mess}**\n Причина: __{reason}__')
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(embed=emb)
    @commands.command(aliases=["разбан"], help = 'unban <USER_ID>')
    @has_permissions(administrator=True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        emb = discord.Embed(description=f'Вы разбанили {user.mention}')
        await ctx.send(embed=emb)
    @commands.command(aliases=["prefix", "prefixset", "pref"], help = 'prefix/set-prefix/setprefix <new prefix>')
    @commands.is_owner()
    async def setprefix(self, ctx, prefix):
        gui = await get_guild_id(ctx)
        with open('cogs/data.json', 'r') as f:
            pref = json.load(f)
        if prefix != pref['servers'][gui]:
            pref['servers'][gui]['prefix'] = prefix
            with open('cogs/data.json', 'w') as f:
                json.dump(pref, f)
            emb = discord.Embed(description=f':white_check_mark: Вы сменили префикс на "**{pref["servers"][gui]["prefix"]}**"')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Префикс "**{pref["servers"][gui]["prefix"]}**" уже используется')
            await ctx.send(embed=emb)
    @commands.command(aliases=["ecoemoji", "seteemoji"], help = 'ecoemoji <new currency emoji>')
    @has_permissions(administrator=True)
    async def ecemoji(self, ctx, emoji):
        with open("cogs/data.json", 'r') as f:
            emojis = json.load(f)
        emo = await get_ecoemoji(ctx)
        if not emoji == emojis['servers'][str(ctx.guild.id)]['ecoemoji']:
            emojis['servers'][str(ctx.guild.id)]['ecoemoji'] = emoji
            with open('cogs/data.json', 'w') as f:
                json.dump(emojis, f)
            emo = await get_ecoemoji(ctx)
            emb = discord.Embed(description=f':white_check_mark: Эмодзи валюты был успешно изменён на {emo}')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'{emo} уже используется в качестве обозначения валюты!')
            await ctx.send(embed=emb)
    @commands.command(aliases=["guild-id"], help = 'guildid')
    @has_permissions(administrator=True)
    async def guildid(self, ctx):
        result = await get_guild_id(ctx)
        await ctx.send(result)
    @commands.command(aliases=["inclear", "clearinventory"], help = 'iclear <@member>')
    @has_permissions(administrator=True)
    async def iclear(self, ctx, member: discord.Member = None):
        clea = await get_data()
        if member == None:
            synt = 'iclear/inclear <@member>'
            await get_error(ctx, synt)
        elif member.id == ctx.author.id:
            clea['servers'][str(ctx.guild.id)]['inv'][str(ctx.author.id)] = {}
            emb = discord.Embed(description=f'**{ctx.author}** очистил свой инвентарь')
            await ctx.send(embed=emb)
        elif member.id != ctx.author.id:
            clea['servers'][str(ctx.guild.id)]['inv'][str(member.id)] = {}
            emb = discord.Embed(description=f'**{ctx.author}** очистил инвентарь **{member}**')
            await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(clea, f)

#Edit Owner Commands
    @commands.command(aliases=["add-owner"])
    @commands.is_owner()
    async def addowner(self, ctx, member: discord.Member):
        with open('cogs/data.json', 'r') as f:
            addown = json.load(f)
        if not member.id == ctx.author.id:
            for owns in addown['owners']:
                if member.id == owns:
                    emb = discord.Embed(description=f':no_entry_sign: {member} already owner!')
                    await ctx.send(embed=emb)
                    exit
            addown['owners'].append(member.id)
            with open('cogs/data.json', 'w') as f:
                json.dump(addown, f)
            emb = discord.Embed(description=f':white_check_mark: {member} became the owner!')
            await ctx.send(embed=emb)
            self.bot.owner_ids = await get_owners()
        else:
            emb = discord.Embed(description=f':no_entry_sign: You already owner!')
            await ctx.send(embed=emb)
    @commands.command(aliases=["del-owner"])
    @commands.is_owner()
    async def delowner(self, ctx, member: discord.Member):
        with open('cogs/data.json', 'r') as f:
            delown = json.load(f)
        if not member.id == ctx.author.id:
            for owns in delown['owners']:
                if member.id == owns:
                    delown['owners'].remove(member.id)
                    with open('cogs/data.json', 'w') as f:
                        json.dump(delown, f)
                    emb = discord.Embed(description=f':no_entry_sign: {member} was removed from the list of owners!')
                    await ctx.send(embed=emb)
                    self.bot.owner_ids = await get_owners()
                    exit
        elif member.id == ctx.author.id:
            delown['owners'].remove(ctx.author.id)
            with open('cogs/data.json', 'w') as f:
                json.dump(delown, f)
            emb = discord.Embed(description=f":no_entry_sign: {member.mention}you have removed yourself from the list of owners!")
            await ctx.send(embed=emb)
            self.bot.owner_ids = await get_owners()
    @commands.command(aliases=["lowner"])
    @has_permissions(administrator=True)
    async def ownerlist(self, ctx):
        with open('cogs/data.json', 'r') as f:
            owners = json.load(f)
        ownlist = []
        for own in owners['owners']:
            ownlist.append(own)
        '\n'.split(str(ownlist))
        emb = discord.Embed(description=f'{ownlist}')
        await ctx.send(ownlist)


    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'say <text>'
            await get_error(ctx, synt)
    @шнюк.error
    async def шнюк_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'шнюк/nuke <quanti> <text>'
            await get_error(ctx, synt)
    @additem.error
    async def additem_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'add-item/additem <name> <quanti> <@member>'
            await get_error(ctx, synt)
    @delitem.error
    async def delitem_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'del-item/delitem <name> <quanti> <@member>'
            await get_error(ctx, synt)
    @addmoney.error
    async def addmoney_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'addmoney/add-money <quanti> <@member>'
            await get_error(ctx, synt)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError):
            synt = 'ban <@member> <reason>'
            await get_error(ctx, synt)
    @delmoney.error
    async def delmoney_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'delmoney/del-money <quanti> <@member>'
            await get_error(ctx, synt)
    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'prefix/set-prefix/setprefix <new prefix>'
            await get_error(ctx, synt)
    @shopaddrole.error
    async def shopaddrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'shop-add-role/sar/shopaddrole <@ROLE> <count> <quanti>'
            await get_error(ctx, synt)
    @shopdelrole.error
    async def shopdelrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'shop-del-role/sdr/shopdelrole <@ROLE> <count>'
            await get_error(ctx, synt)
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'unban <USER_ID>'
            await get_error(ctx, synt)
    @iclear.error
    async def iclear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'iclear <@member>'
            await get_error(ctx, synt)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'clear <count>'
            await get_error(ctx, synt)



def setup(bot):
    bot.add_cog(Admin(bot))