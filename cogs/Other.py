import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *



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
    @commands.command(aliases=["топ"], help = 'top <count>')
    async def top(self, ctx, quanti: int = 5):
        with open('cogs/data.json', 'r') as f:
            top = json.load(f)
        emo = await get_ecoemoji(ctx)
        nam = []
        mon = []
        for member in top['servers'][str(ctx.guild.id)]['money']:
            nam.append(top['servers'][str(ctx.guild.id)]['money'][str(member)]['Name'])
            mon.append(top['servers'][str(ctx.guild.id)]['money'][str(member)]['Money'])
        qu = len(nam)
        if quanti > qu:
            quanti = qu
        mon.sort(reverse=True)
        i = 0
        msg = ''
        while i < qu:
            for member in top['servers'][str(ctx.guild.id)]['money']:
                if i >= quanti:
                    i += 1
                    pass
                elif mon[i] == top['servers'][str(ctx.guild.id)]['money'][str(member)]['Money']:
                    if i <= 2:
                        msg += '**{0}. {1} — {2} {3}**\n'.format(i+1, top['servers'][str(ctx.guild.id)]["money"][str(member)]["Name"], top['servers'][str(ctx.guild.id)]["money"][str(member)]["Money"], emo)
                    if i > 2:
                        msg += '{0}. {1} — {2} {3}\n'.format(i+1, top['servers'][str(ctx.guild.id)]["money"][str(member)]["Name"], top['servers'][str(ctx.guild.id)]["money"][str(member)]["Money"], emo)
                    i += 1
                else:
                    pass
        emb = discord.Embed(title=f'Список лидеров {emo}', description=msg)
        await ctx.send(embed=emb)
    @commands.command()
    async def last(self, ctx, member: discord.Member = None):
        mess = await last_mess(ctx, member)
        await ctx.send(f'Ваше последнее сообщение: {mess.content}')
    @commands.command()
    async def test(self, ctx):
        comms = ''
        cog = self.bot.get_cog('Economic')
        for name, func in cog.get_listeners():
            await ctx.send(f'{name} -> {func}\n')
            comms += f'{name} -> {func}\n'
        

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'poll <title>\nemoji - text\nemoji - text\n...'
            await get_error(ctx, synt)
    @emb.error
    async def emb_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            synt = 'emb <title> <color> <quantity of fields> name / text / inline: true(false) / name / text / inline: true(false) / .......'
            await get_error(ctx, synt)


def setup(bot):
    bot.add_cog(Other(bot))