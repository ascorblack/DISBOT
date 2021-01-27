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


    # @commands.command(help = 'wages \nПолучить деньги')
    # async def wages(self, ctx):
    #     emo = await get_ecoemoji(ctx)
    #     if not str(ctx.author.id) in self.bot.queue:
    #         emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои 150 {emo}\nСледующее получение будет доступно только через 2 минуты')
    #         await ctx.send(embed=emb)
    #         member = ctx.author
    #         await up_money(ctx, member, co = +150)
    #         db.commit()
    #         self.bot.queue.append(str(ctx.author.id))
    #         await asyncio.sleep(120)
    #         self.bot.queue.remove(str(ctx.author.id))
    #     if str(ctx.author.id) in self.bot.queue:
    #         emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
    #         await ctx.send(embed=emb)
    @commands.command(aliases=["баланс", "bal"], help = 'balance <@member>')
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
    @commands.command(aliases=["give"], help = 'give/transfer <@member> <item-name> <quantity>')
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
    bot.add_cog(Economic(bot))