import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from mongo import *


class Admin(commands.Cog):
    """Commands for Administrators and Owners only"""
    def __init__(self, bot):
        self.bot = bot
        self.bal = bal
        self.pref = pref
        self.owners = owners
        self.ecoemoji = ecoemoji
        self.welcch = welcch
        self.exitch = exitch
        self.newschan = newschan
        

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
            await ctx.send('Выключаюсь...')
            await self.bot.logout()
    @commands.command(aliases=["чистка"], help = 'clear <count>')
    @has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        emb = discord.Embed(color=discord.Colour.dark_grey(), description='Было отчищенно ' + str(amount) + ' сообщений!')
        await ctx.send(embed=emb)
    @commands.command(aliases=["spam"], help = 'шнюк/spam <quanti> <text>')
    @has_permissions(administrator=True)
    async def шнюк(self, ctx, k, *, text):
        mess = await get_last_mess(ctx, member = None)
        await mess.delete()
        i = 0
        while i < int(k):
            await ctx.send(text)
            i += 1
    # @commands.command(aliases=["нюк"], hidden = True)
    # @commands.is_owner()
    # async def nuke(self, ctx):
    #     emb = discord.Embed(description=f'{ctx.author} Ты уверен?', color = discord.Colour.red())
    #     warn = await ctx.send(embed=emb)
    #     emoji = '🔛'
    #     await warn.add_reaction(emoji)
    #     def check(reaction, user):
    #         return str(reaction.emoji) == emoji and user.id == ctx.author.id
    #     try:
    #         reaction, user = await self.bot.wait_for("reaction_add", timeout=3, check=check)
    #         emb = discord.Embed(description=f'{ctx.author} начал полное уничтожение сервера!', color = discord.Colour.red())
    #         await warn.edit(embed=emb)
    #         for member in ctx.guild:
    #             if not member.bot:
    #                 if member != ctx.author:
    #                     await ctx.guild.ban(member, reason='😈 СЕРВЕР ЗАХВАЧЕН!')
    #     except asyncio.TimeoutError:
    #         emb = discord.Embed(description=f'{ctx.author} не успел активировать бомбу', color = discord.Colour.green())
    #         await warn.edit(embed=emb)
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
            if member == None or str(member.id) == str(ctx.author.id):
                member = ctx.author
                await up_money(ctx, member, co = +qu)
                emb = discord.Embed(description=f'Вы добавили на свой счёт {qu} {emo}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
            else:
                await up_money(ctx, member, co = +qu)
                emb = discord.Embed(description=f'Вы добавили на счёт **{member}** {qu} {emo}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете добавить отрицательно/нулевое количество {emo}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["удалить-деньги", "del-money"], help = 'delmoney/del-money <quanti> <@member>')
    @has_permissions(administrator=True)
    async def delmoney(self, ctx, qu: int, member: discord.Member = None):
        emo = await get_ecoemoji(ctx)
        if qu > 0:
            if member == None or str(member.id) == str(ctx.author.id):
                member = ctx.author
                bal = await get_money(ctx, member)
                if bal == None and not member.bot:
                    await add_bal_user(ctx, member)
                    bal = await get_money(ctx, member)
                await up_money(ctx, member, co = -qu)
                emb = discord.Embed(description=f'Вы удалили со своего счёта {qu} {emo}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
            else:
                bal = await get_money(ctx, member)
                if bal == None and not member.bot:
                    await add_bal_user(ctx, member)
                    bal = await get_money(ctx, member)
                await up_money(ctx, member, co = -qu)
                emb = discord.Embed(description=f'Вы удалили со счёта **{member}** {qu} {emo}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете удалить отрицательно/нулевое количество {emo}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["бан"], help = 'ban <@member> <reason>')
    @has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member = None, reason = None):
        mess = str(member)
        if str(member.id) == str(ctx.author.id):
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
    async def setprefix(self, ctx, prefix: str):
        pref = await get_prefixes(ctx)
        if len(prefix) > 5:
            emb = discord.Embed(description=':no_entry_sign: Префикс не может быть длиннее 5 символов!')
            await ctx.send(embed=emb)
        elif prefix == pref:
            emb = discord.Embed(description=f':no_entry_sign: Префикс **{prefix}** уже используется!')
            await ctx.send(embed=emb)
        else:
            self.pref.update_one({"GuildID": ctx.guild.id},{"$set": {"Prefix": str(prefix)}})
            emb = discord.Embed(description=f':white_check_mark: Вы сменили префикс на "**{prefix}**"')
            await ctx.send(embed=emb)
    @commands.command(aliases=["ecoemoji", "seteemoji"], help = 'ecoemoji <new currency emoji>')
    @has_permissions(administrator=True)
    async def ecemoji(self, ctx, emoji):
        emo = await get_ecoemoji(ctx)
        if not emoji == emo:
            self.ecoemoji.update_one({"GuildID": ctx.guild.id},{"$set": {"Emoji": str(emoji)}})
            emo = await get_ecoemoji(ctx)
            emb = discord.Embed(description=f':white_check_mark: Эмодзи валюты был успешно изменён на {emo}')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: {emo} уже используется в качестве обозначения валюты!')
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

#Join/leave member commands
    @commands.command(help = 'setwelc <channelID>')
    @has_permissions(administrator=True)
    async def setwelc(self, ctx, channel: int):
        found = False
        for chann in ctx.guild.text_channels:
            channi = chann.id
            if channel == channi:
                found = True
                check = self.welcch.find_one({"GuildID": ctx.guild.id})['ChannelID']
                if check == 0 or check != channel:
                    self.welcch.update_one({"GuildID": ctx.guild.id}, {"$set": {"ChannelID": channel}})
                    emb = discord.Embed(description=f':white_check_mark: Канал **{chann}** был назначен для приветствий!')
                    await ctx.send(embed=emb)
                elif check != 0 and check == channel:
                    emb = discord.Embed(description=f':no_entry_sign: Канал **{chann}** уже назначен для приветствий!')
                    await ctx.send(embed=emb)
            else:
                pass
        if not found:
            emb = discord.Embed(description=f':no_entry_sign: Введите корректный **текстовый** канал!')
            await ctx.send(embed=emb)
    @commands.command(help = 'setexit <channelID>')
    @has_permissions(administrator=True)
    async def setexit(self, ctx, channel: int):
        found = False
        for chann in ctx.guild.text_channels:
            channi = chann.id
            if channel == channi:
                found = True
                check = self.exitch.find_one({"GuildID": ctx.guild.id})['ChannelID']
                if check == 0 or check != channel:
                    self.exitch.update_one({"GuildID": ctx.guild.id}, {"$set": {"ChannelID": int(channi)}})
                    emb = discord.Embed(description=f':white_check_mark: Канал **{chann}** был назначен для прощаний!')
                    await ctx.send(embed=emb)
                elif check != 0 and check == channel:
                    emb = discord.Embed(description=f':no_entry_sign: Канал **{chann}** уже назначен для прощаний!')
                    await ctx.send(embed=emb)
            else:
                pass
        if not found:
            emb = discord.Embed(description=f':no_entry_sign: Введите корректный **текстовый** канал!')
            await ctx.send(embed=emb)
    @commands.command(help = 'setwelcmsg *message')
    @has_permissions(administrator=True)
    async def setwelcmsg(self, ctx, *, msg):
        if msg != None:
            self.welcch.update_one({"GuildID": ctx.guild.id}, {"$set": {"Message": str(msg)}})
            emb = discord.Embed(description=f':white_check_mark: Сообщение приветствия изменено на:\n{msg}')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Введите новый текст приветствия!')
            await ctx.send(embed=emb)
    @commands.command(help = 'setexitmsg *message')
    @has_permissions(administrator=True)
    async def setexitmsg(self, ctx, *, msg):
        if msg != None:
            self.exitch.update_one({"GuildID": ctx.guild.id}, {"$set": {"Message": str(msg)}})
            emb = discord.Embed(description=f':white_check_mark: Сообщение прощания изменено на:\n{msg}')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Введите новый текст прощания!')
            await ctx.send(embed=emb)

#Edit Owner Commands
    @commands.command(aliases=["add-owner"])
    @commands.is_owner()
    async def addowner(self, ctx, member: discord.Member):
        ows = await get_owners()
        if not member.id == ctx.author.id:
            for owns in ows:
                if member.id == owns:
                    emb = discord.Embed(description=f':no_entry_sign: {member} already owner!')
                    await ctx.send(embed=emb)
                    exit
            self.owners.insert_one({"MemberID": member.id, "Owner": True})
            self.bot.owner_ids = await get_owners()
            emb = discord.Embed(description=f':white_check_mark: {member} became the owner!')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: You already owner!')
            await ctx.send(embed=emb)
    @commands.command(aliases=["del-owner"])
    @commands.is_owner()
    async def delowner(self, ctx, member: discord.Member):
        ows = await get_owners()
        if not member.id == ctx.author.id:
            for owns in ows:
                if member.id == owns:
                    self.owners.remove({"MemberID": member.id})
                    emb = discord.Embed(description=f':no_entry_sign: {member} was removed from the list of owners!')
                    await ctx.send(embed=emb)
                    self.bot.owner_ids = await get_owners()
                    exit
        elif member.id == ctx.author.id:
            self.owners.remove({"MemberID": ctx.author.id})
            emb = discord.Embed(description=f":no_entry_sign: {member.mention}you have removed yourself from the list of owners!")
            await ctx.send(embed=emb)
            self.bot.owner_ids = await get_owners()
    @commands.command(aliases=["lowner"])
    @has_permissions(administrator=True)
    async def ownerlist(self, ctx):
        msg = ''
        ows = await get_owners()
        for own in ows:
            msg += f'{own}\n'
        emb = discord.Embed(description=msg)
        await ctx.send(embed=emb)


# Установить канал для новостей
    @commands.command(aliases=['setnewsch', "newsetchan"])
    @has_permissions(administrator=True)
    async def news_set_channel(self, ctx, channel: int):
        found = False
        for chann in ctx.guild.text_channels:
            channi = chann.id
            if channel == channi:
                check = self.newschan.find_one({"GuildID": ctx.guild.id})['ChannelID']
                if check == 0 or check != channel:
                    self.newschan.update_one({"GuildID": ctx.guild.id}, {"$set": {"ChannelID": channel}})
                    emb = discord.Embed(description=f'В качестве канала, для постинга новостей вы установили **{chann.name}**', color=await hid_emb())
                    await ctx.send(embed=emb)
                elif check != 0 and check == channel:
                    emb = discord.Embed(description=f':no_entry_sign: Канал **{chann}** уже назначен для новостей!')
                    await ctx.send(embed=emb)
                return
            else:
                pass
        if not found:
            emb = discord.Embed(description=f':no_entry_sign: Введите корректный **текстовый** канал!')
            await ctx.send(embed=emb)



def setup(bot):
    bot.add_cog(Admin(bot))