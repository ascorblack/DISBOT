import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import * 


class Economic(commands.Cog):
    """Economic commands"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["зп"], help = 'wages')
    async def wages(self, ctx):
        emo = await get_ecoemoji(ctx)
        if not str(ctx.author.id) in self.bot.queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои 150 {emo}\nСледующее получение будет доступно только через 2 минуты')
            await ctx.send(embed=emb)
            member = ctx.author
            await up_money(ctx, member, co = +150)
            db.commit()
            self.bot.queue.append(str(ctx.author.id))
            await asyncio.sleep(120)
            self.bot.queue.remove(str(ctx.author.id))
        if str(ctx.author.id) in self.bot.queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed=emb)
    @commands.command(aliases=["баланс", "bal"], help = '-balance <@member>')
    async def balance(self, ctx, member: discord.Member = None):
        emo = await get_ecoemoji(ctx)
        if member == None:
            member = ctx.author
            bal = await get_money(ctx, member)
            if bal == None and not member.bot:
                await add_bal_user(ctx, member)
                db.commit()
                bal = await get_money(ctx, member)
            if bal == None and member.bot:
                emb = discord.Embed(description=f'У **{member}** на счету не может быть {emo}, так как он Бот! ', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У вас на счету {bal} {emo}', color=discord.Colour.dark_green())
                emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=emb)
        else:
            bal = await get_money(ctx, member)
            if bal == None and not member.bot:
                await add_bal_user(ctx, member)
                db.commit()
                bal = await get_money(ctx, member)
            if bal == None and member.bot:
                emb = discord.Embed(description=f'У **{member}** на счету не может быть {emo}, так как он Бот! ', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=f'У **{member}** на счету {bal} {emo}', color=discord.Colour.dark_green())
                emb.set_author(name=member.name, icon_url=member.avatar_url)
                await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Economic(bot))