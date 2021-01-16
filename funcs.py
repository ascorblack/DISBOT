from config import settings
import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, HelpCommand, Command
import asyncio

async def get_guild_id(ctx):
    ID = str(ctx.guild.id)
    return ID

async def get_er_mis(ctx, error):
        with open("cogs/data.json", 'r') as f:
            prefixes = json.load(f)
        pref = prefixes['servers'][str(ctx.guild.id)]['prefix']
        emb = discord.Embed(description=f':no_entry_sign: Неверный синтаксис!\nИспользуй {prefix}commands', color=discord.Colour.red())
        return emb

async def get_error(ctx, error, synt):
        with open("cogs/data.json", 'r') as f:
            prefixes = json.load(f)
        pref = prefixes['servers'][str(ctx.guild.id)]['prefix']
        emb = discord.Embed(description=f':no_entry_sign: Неверный синтаксис!\nИспользуй {pref}{synt}', color=discord.Colour.red())
        return await ctx.send(embed=emb)

async def last_mess(ctx, member: discord.Member = None):
    if member == None or member == ctx.author.id:
        lmess = await ctx.channel.history().find(lambda m: m.author.id == ctx.author.id)
        if (lmess is not None):
            return lmess
    else:
        lmess = await ctx.channel.history().find(lambda m: m.author.id == member.id)
        if (lmess is not None):
            return lmess


# async def get_guild(ctx):
#     with open("cogs/data.json", 'r') as f:
#         prefixes = json.load(f)
#     return prefixes['servers'][str(ctx.guild.id)]
async def get_ecoemoji(guild):
    with open("cogs/data.json", 'r') as f:
        prefixes = json.load(f)
    emoji = prefixes['servers'][str(guild.id)]['ecoemoji']
    return str(emoji)