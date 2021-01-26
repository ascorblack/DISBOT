import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from time import time
from datetime import date, timedelta, datetime


class Other(commands.Cog):
    """Other interesting commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cocy(self, ctx):
        rand = random.randint(1, 100)
        if rand < 50:
            await ctx.send('Ну и соси :rage:')
        else:
            await ctx.send('Не в этот раз :smiling_imp: ')
    @commands.command(aliases=["аватар"], help = 'avatar <@member>')
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            emb = discord.Embed(title=f'Аватарка {ctx.author}')
            emb.set_image(url='{}'.format(ctx.author.avatar_url))
            await ctx.send(embed=emb)
        elif member != None:
            emb = discord.Embed(title=f'Аватарка {member}')
            emb.set_image(url='{}'.format(member.avatar_url))
            await ctx.send(embed=emb)
    @commands.command(help = 'emb <title> <color> <quantity of fields> name / text / inline: true(false) / name / text / inline: true(false) / .......')
    async def emb(self, ctx, title, color: discord.Colour = None, q: int = None, *, atr=None):
        if atr == None and q <= 1:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(title=f'{title}', color=color)
            await ctx.send(embed=emb)
        elif atr != None:
            atr = atr.split(' / ')
            n = 0
            i = 0
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(title=f'{title}', color=color)
            if q > 1:
                name = 0
                value = 1
                inline = 2
                while i < q:
                    emb.add_field(name=f'{atr[name]}', value=f'{atr[value]}', inline=atr[inline])
                    name += 3
                    value += 3
                    inline += 3
                    i += 1
                await ctx.send(embed=emb)
            else:
                nn = atr[n]
                nv = atr[n+1]
                ni = atr[n+2]
                emb.add_field(name=f'{nn}', value=f'{nv}', inline=ni)
                await ctx.send(embed=emb)
        # emb.add_field(name=f'{nn}', value=f'{nv}', inline=ni)
        # i += 1
        # await ctx.send(embed=emb)
    @commands.command(help = 'poll <title>\nemoji - text\nemoji - text\n...')
    async def poll(self, ctx, *, atr):
        art = atr.split('\n')
        title = art[0]
        x = art[0]
        art.remove(x)
        des = '\n'.join(art)
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title=f'{title}', description=f'{des}', color=discord.Colour.orange())
        mess = await ctx.send(embed=emb)
        for polls in art:
            if polls.find('-'):
                poll = polls.split('-')
                emoji = poll[0].strip()
                await mess.add_reaction(emoji)
    @commands.command(aliases=["топ"], help = 'top (<count> - default 5)')
    async def top(self, ctx, quanti = 5):
        emo = await get_ecoemoji(ctx)
        msg = ''
        ball = ''
        namm = ''
        bal = db.records("SELECT Money FROM balance WHERE GuildID = ? ORDER BY Money DESC", ctx.guild.id)
        name = db.records("SELECT MemberName FROM balance WHERE GuildID = ? ORDER BY Money DESC", ctx.guild.id)
        qu = len(bal)
        if quanti > qu:
            quanti = qu
        i = 0
        while i < qu:
            if i >= quanti:
                i += 1
                pass
            else:
                ball += f'{bal[i]}'
                namm += f'{name[i]}'
                if i <= 2:
                    msg += '**{0}. {1} — {2} {3}**\n'.format(i+1, namm[2:-3], ball[1:-2], emo)
                if i > 2:
                    msg += '{0}. {1} — {2} {3}\n'.format(i+1, namm[2:-3], ball[1:-2], emo)
                ball = ''
                namm = ''
                i += 1
        emb = discord.Embed(title=f'**{ctx.guild.name}** | Топ лидеров {emo}', description=f'{msg}', color = discord.Colour.blue())
        await ctx.send(embed=emb)
    @commands.command()
    async def last(self, ctx, member: discord.Member = None):
        mess = await last_mess(ctx, member)
        await ctx.send(f'Ваше последнее сообщение: {mess.content}')
    @commands.command(aliases=["пинг"], help = 'ping/пинг')
    async def ping(self, ctx):
        start = time()
        msg = await ctx.send(f'Понг! Задержка: {round(self.bot.latency * 1000)} мс')
        end = time()
        await msg.edit(content=f'Понг! Задержка: `{round(self.bot.latency * 1000)} мс`.\nВремя ответа: `{-round((start - end) * 1000)} мс`')
    @commands.command(help = 'stat \nдемо-версия')
    async def stat(self, ctx):
        now = datetime.utcnow()
        t14 = now - timedelta(days=14)
        t7 = now - timedelta(days=7)
        t1 = now - timedelta(days=1)
        c14 = 0
        c7 = 0
        c1 = 0
        for channel in ctx.guild.text_channels:
            async for msg in channel.history(after=t14, limit=None):
                if msg.author.id == ctx.author.id:
                    c14 += 1
            async for msg in channel.history(after=t7, limit=None):
                if msg.author.id == ctx.author.id:
                    c7 += 1
            async for msg in channel.history(after=t1, limit=None):
                if msg.author.id == ctx.author.id:
                    c1 += 1
        emb = discord.Embed(title=f'{ctx.author}', color = discord.Colour.random())
        emb.add_field(name = 'Пользовательская информация', value=f'Присоединился к серверу: `{ctx.author.joined_at.strftime("%d.%m.%Y (%H:%M)")}`\nСоздал аккаунт: `{ctx.author.created_at.strftime("%d.%m.%Y (%H:%M)")}`\nID: `{ctx.author.id}`', inline=False)
        emb.add_field(name='Сообщения', value=f'За 14 дней: `{c14} сообщений`\nЗа 7 дней: `{c7} сообщений`\nЗа последние 24 часа: `{c1} сообщений`')
        emb.add_field(name='Топ роль', value=f'**{ctx.author.top_role}**')
        emb.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=emb)



def setup(bot):
    bot.add_cog(Other(bot))