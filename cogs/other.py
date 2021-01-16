import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *



class _Other_(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cocy(self, ctx):
        rand = random.randint(1, 100)
        if rand < 50:
            await ctx.send('Ну и соси :rage:')
        else:
            await ctx.send('Не в этот раз :smiling_imp: ')
    # @commands.command(aliases=["help"])
    # async def помощь(self, ctx, command=None):
    #     if command != None:
    #         out = await 
    #         emb = discord.Embed(color=discord.Colour.dark_gold(), description=f'{out}')
    #         await ctx.send(embed=emb)
        # if help == 'перестрелка':
        #     emb = discord.Embed(title='Форма заполнения "-перестрелка":', color=discord.Colour.red(),
        #                 description='\nЕСЛИ НУЖНО, ЧТОБЫ ИМЯ СОДЕРЖАЛО БОЛЬШЕ ОДНОГО СЛОВА,Т.Е. ИМЕЛО ПРОБЕЛ, НУЖНО ЗАКЛЮЧИТЬ В __**КАВЫЧКИ**__! ("Джо Байден")'
        #             '\n\n-перестрелка (Имя 1-ого игрока) (Имя 2-ого игрока) (Кол-во патронов 1-ого Игрока) (Кол-во патронов 2-ого Игрока)'
        #             '\n\n**Правила увеличения шанса:**\nЕсли у игрока N патронов больше на 5-14, то его шанс выиграть увеличивается на 15%, если же разница больше 15, то на 25%')
        #     await ctx.send(embed=emb)
        # elif help == 'шнюк':
        #     emb = discord.Embed(title='Инструкция по спам шнюку:', color=discord.Colour.dark_gold(), description='\n-шнюк (кол-во повторений) (любой текст)')
        #     await ctx.send(embed=emb)
        # elif help == 'дуэль':
        #     emb = discord.Embed(title='Инструкция по комманде "-дуэль":', color=discord.Colour.blurple(), description='\n-дуэль (Имя 1-ого игрока) (Имя 2-ого игрока)'
        #                 '\n\nЕСЛИ НУЖНО, ЧТОБЫ ИМЯ СОДЕРЖАЛО БОЛЬШЕ ОДНОГО СЛОВА,Т.Е. ИМЕЛО ПРОБЕЛ, НУЖНО ЗАКЛЮЧИТЬ В __**КАВЫЧКИ**__! ("Джо Байден")')
        #     await ctx.send(embed=emb)
        # else:
        #     exit
    @commands.command(aliases=["аватар"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            emb = discord.Embed(description=f'Неккоректные данные!')
            await ctx.send(embed=emb)
        elif member != None:
            emb = discord.Embed(title=f'Аватарка {member}')
            emb.set_image(url='{}'.format(member.avatar_url))
            await ctx.send(embed=emb)
    @commands.command()
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
    @commands.command()
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
    @commands.command(aliases=["топ"])
    async def top(self, ctx, quanti: int = 5):
        with open('cogs/data.json', 'r') as f:
            top = json.load(f)
        nam = []
        mon = []
        for member in top['money']:
            nam.append(top['money'][str(member)]['Name'])
            mon.append(top['money'][str(member)]['Money'])
        qu = len(nam)
        if quanti > qu:
            quanti = qu
        mon.sort(reverse=True)
        i = 0
        msg = ''
        while i < qu:
            for member in top['money']:
                if i >= quanti:
                    i += 1
                    pass
                elif mon[i] == top['money'][str(member)]['Money']:
                    if i <= 2:
                        msg += '**{0}. {1} — {2} {3}**\n'.format(i+1, top["money"][str(member)]["Name"], top["money"][str(member)]["Money"], self.bot.eco_emoji)
                    if i > 2:
                        msg += '{0}. {1} — {2} {3}\n'.format(i+1, top["money"][str(member)]["Name"], top["money"][str(member)]["Money"], self.bot.eco_emoji)
                    i += 1
                else:
                    pass
        emb = discord.Embed(title=f'Список лидеров {self.bot.eco_emoji}', description=msg)
        await ctx.send(embed=emb)
    @commands.command()
    async def last(self, ctx, member: discord.Member = None):
        mess = await last_mess(ctx, member)
        await ctx.send(f'Ваше последнее сообщение: {mess}')


    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'poll <title>\nemoji - text\nemoji - text\n...'
            await get_error(ctx, error, synt)
    @emb.error
    async def emb_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'emb <title> <color> <quantity of fields> name / text / inline: true(false) / name / text / inline: true(false) / .......'
            await get_error(ctx, error, synt)


def setup(bot):
    bot.add_cog(_Other_(bot))