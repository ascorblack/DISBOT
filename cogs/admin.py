import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import guild_id
from funcs import _test


class _Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop', aliases=["стоп"], pass_context=True)
    @has_permissions(administrator=True)
    async def stop(self, ctx):
            await ctx.send('Ну ББ, KEKW')
            await self.bot.logout()
    @commands.command(aliases=["clear"])
    @has_permissions(administrator=True)
    async def чистка(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        emb = discord.Embed(color=discord.Colour.dark_grey(), description='Было отчищенно ' + str(amount) + ' сообщений!')
        await ctx.send(embed=emb)
    @commands.command(aliases=["spam"])
    @commands.has_any_role("Повелитель")
    async def шнюк(self, ctx, k, *, text):
        await ctx.channel.purge(limit=1)
        i = 0
        while i < int(k):
            await ctx.send(text)
            i += 1
    @commands.command(aliases=["nuke"])
    @commands.has_any_role("Повелитель")
    async def нюк(self, ctx):
        await ctx.send('https://tenor.com/view/destory-eexplode-nuke-gif-6073338')
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, text):
        await ctx.channel.purge(limit=1)
        await ctx.send(text)
    @commands.command(aliases=["добавить-предмет", "add-item"])
    @has_permissions(administrator=True)
    async def добавить_предмет(self, ctx, name, qu: int, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            add = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in add['inv']:
                add['inv'][str(ctx.author.id)] = {}
            if not name in add['inv'][str(ctx.author.id)]:
                add['inv'][str(ctx.author.id)][name] = {}
                add['inv'][str(ctx.author.id)][name]['quanti'] = qu
                emb = discord.Embed(description=f':white_check_mark: Вы добавили предмет "{name}" в количестве {str(qu)}')
                await ctx.send(embed=emb)
                if add['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
            else:
                add['inv'][str(ctx.author.id)][name]['quanti'] += qu
                if qu < 0:
                    emb = discord.Embed(description=f':white_check_mark: Вы уменьшили количество предмета "{name}" на {str(-qu)}')
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(description=f':white_check_mark: Вы увеличили количество предмета "{name}" на {str(qu)}')
                    await ctx.send(embed=emb)
                if add['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
        else:
            if not str(member.id) in add['inv']:
                add['inv'][str(member.id)] = {}
            if not name in add['inv'][str(member.id)]:
                add['inv'][str(member.id)][name] = {}
                add['inv'][str(member.id)][name]['quanti'] = qu
                with open('cogs/data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы добавили **{member}** предмет "{name}", теперь у него {add["inv"][str(member.id)][name]["quanti"]} "{name}"')
                await ctx.send(embed=emb)
            else:
                add['inv'][str(member.id)][name]['quanti'] += qu
                with open('cogs/data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы прибавили **{member}** {qu} предмета "{name}"\nТеперь у него {add["inv"][str(member.id)][name]["quanti"]} "{name}"')
                await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(add, f)
    @commands.command(aliases=["удалить-предмет", "del-item"])
    @has_permissions(administrator=True)
    async def удалить_предмет(self, ctx, name, qu=754325616, member: discord.Member = None):
        with open('cogs/data.json', 'r') as f:
            rem = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not name in rem['inv'][str(ctx.author.id)]:
                await ctx.send(':no_entry_sign: у вас нет такого предмета в инвентаре!')
                exit
            else:
                if qu <= 0:
                    await ctx.send(':no_entry_sign: Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu == 754325616:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(ctx.author.id)][name]
                elif qu >= rem['inv'][str(ctx.author.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(ctx.author.id)][name]
                else:
                    rem['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(qu)} предмета "{name}"')
                    await ctx.send(embed=emb)
        elif member != str(ctx.author.id):
            if not name in rem['inv'][str(member.id)]:
                emb = discord.Embed(description=f'У {member.mention} нет такого предмета в инвентаре')
                await ctx.send(embed=emb)
                exit
            else:
                if qu <= 0:
                    await ctx.send('Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu >= rem['inv'][str(member.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(rem["inv"][str(member.id)][name]["quanti"])} "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(member.id)][name]
                else:
                    rem['inv'][str(member.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(qu)} "{name}"')
                    await ctx.send(embed=emb)
        with open('cogs/data.json', 'w') as f:
            json.dump(rem, f)
    @commands.command(aliases=["выставить-роль", "add-role"])
    @has_permissions(administrator=True)
    async def выставить_роль(self, ctx, role: discord.Role, cost: int, quant=1):
        if quant <= 0:
            await ctx.send(':no_entry_sign: Невозможно выставить отрицательное/нулеовое кол-во слотов!')
            pass
        else:
            with open('cogs/data.json', 'r') as f:
                add = json.load(f)
            if str(role.id) in add['shop']:
                await ctx.send(":no_entry_sign: Эта роль уже есть в магазине")
            if not str(role.id) in add['shop']:
                add['shop']['Role'][str(role.id)] = {}
                add['shop']['Role'][str(role.id)]['Cost'] = cost
                add['shop']['Role'][str(role.id)]['Quant'] = quant
                await ctx.send(f':white_check_mark: Роль добавлена в магазин {role}')
            with open('cogs/data.json', 'w') as f:
                json.dump(add, f)
    @commands.command(aliases=["удалить-роль", "del-role"])
    @has_permissions(administrator=True)
    async def удалить_роль(self, ctx, role: discord.Role, quant=None):
        if quant == None:
            with open('cogs/data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove['shop']['Role']:
                await ctx.send(":no_entry_sign: Этой роли нет в магазине")
            if str(role.id) in remove['shop']['Role']:
                await ctx.send(':white_check_mark: Роль удалена из магазина')
                del remove['shop']['Role'][str(role.id)]
            with open('cogs/data.json', 'w') as f:
                json.dump(remove, f)
        else:
            with open('cogs/data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove['shop']['Role']:
                await ctx.send(":no_entry_sign: Этой роли нет в магазине")
            if int(quant) > remove['shop']['Role'][str(role.id)]['Quant']:
                with open('cogs/data.json', 'r') as f:
                    remove = json.load(f)
                if str(role.id) in remove['shop']['Role']:
                    await ctx.send(':white_check_mark: Роль удалена из магазина')
                    del remove['shop']['Role'][str(role.id)]
                with open('cogs/data.json', 'w') as f:
                    json.dump(remove, f)
            else:
                if str(role.id) in remove['shop']['Role']:
                    remove['shop']['Role'][str(role.id)]['Quant'] -= int(quant)
                    await ctx.send(':white_check_mark:  ' + str(quant) + ' выставленных слотов роли было удалено из магазина')
                with open('cogs/data.json', 'w') as f:
                    json.dump(remove, f)
    @commands.command(aliases=["добавить-деньги", "add-money"])
    @has_permissions(administrator=True)
    async def добавить_деньги(self, ctx, qu: int, member: discord.Member = None):
        if qu > 0:
            with open('cogs/data.json', 'r') as f:
                money = json.load(f)
            if str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money['money']:
                    money['money'][str(ctx.author.id)] = {}
                    money['money'][str(ctx.author.id)]['Money'] = 0
                    money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
                if str(member.id) in money['money']:
                    money['money'][str(ctx.author.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на свой счёт {qu} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money['money']:
                    money['money'][str(member.id)] = {}
                    money['money'][str(member.id)]['Money'] = 0
                    money['money'][str(member.id)]['Name'] = str(member)
                if str(member.id) in money['money']:
                    money['money'][str(member.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на счёт **{member}** {qu} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете добавить отрицательно/нулевое количество {self.bot.eco_emoji}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["удалить-деньги", "del-money"])
    @has_permissions(administrator=True)
    async def удалить_деньги(self, ctx, qu: int, member: discord.Member = None):
        if qu > 0:
            with open('cogs/data.json', 'r') as f:
                money = json.load(f)
            if str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money['money']:
                    money['money'][str(ctx.author.id)] = {}
                    money['money'][str(ctx.author.id)]['Money'] = 0
                    money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
                if str(member.id) in money['money']:
                    money['money'][str(ctx.author.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со своего счёта {qu} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money['money']:
                    money['money'][str(member.id)] = {}
                    money['money'][str(member.id)]['Money'] = 0
                    money['money'][str(member.id)]['Name'] = str(member)
                if str(member.id) in money['money']:
                    money['money'][str(member.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со счёта **{member}** {qu} {self.bot.eco_emoji}', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('cogs/data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете удалить отрицательно/нулевое количество {self.bot.eco_emoji}', color=discord.Colour.red())
            await ctx.send(embed=emb)
    @commands.command(aliases=["бан"])
    @commands.has_any_role("Повелитель")
    async def ban(self, ctx, member: discord.User = None, reason = None):
        mess = member.name
        if member == None or str(member.id) == str(ctx.author.id):
            emb = discord.Embed(description=f'<@{ctx.author.id}> Дурак совсем?')
            await ctx.send(embed=emb)
            exit
        if reason == None:
            reason = "по рофлу"
        emb = discord.Embed(description=f'Вы забанили **{mess}**\n Причина: __{reason}__')
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(embed=emb)
    @commands.command(aliases=["разбан"])
    @commands.has_any_role("Повелитель")
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        emb = discord.Embed(description=f'Вы разбанили {user.mention}')
        await ctx.send(embed=emb)
    @commands.command(aliases=["setprefix", "prefixset", "pref"])
    @commands.is_owner()
    async def prefix(self, ctx, prefix):
        with open('cogs/data.json', 'r') as f:
            pref = json.load(f)
        if prefix != pref['servers'][str(ctx.guild.id)]:
            pref['servers'][str(ctx.guild.id)]['prefix'] = prefix
            with open('cogs/data.json', 'w') as f:
                json.dump(pref, f)
            emb = discord.Embed(description=f':white_check_mark: Вы сменили префикс на "**{pref["servers"][str(ctx.guild.id)]["prefix"]}**"')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Префикс "**{pref["servers"][str(ctx.guild.id)]["prefix"]}**" уже используется')
            await ctx.send(embed=emb)
    @commands.command(aliases=["ecoemoji"])
    @commands.is_owner()
    async def ecemoji(self, ctx, emoji):
        if not emoji == self.bot.eco_emoji:
            self.bot.eco_emoji = emoji
            emb = discord.Embed(description=f':white_check_mark: Эмодзи валюты был успешно изменён на {self.bot.eco_emoji} до конца сеанса')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'{self.bot.eco_emoji} уже используется в качестве обозначения валюты!')
            await ctx.send(embed=emb)
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, msg):
        await ctx.send(_test(msg))


def setup(bot):
    bot.add_cog(_Admin(bot))