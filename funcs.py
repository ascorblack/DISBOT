from config import settings
import json
import random
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, HelpCommand, Command
import asyncio
import time
import os
from mongo import *


async def get_guild_id(ctx):
    ID = str(ctx.guild.id)
    return ID

async def get_er_mis(ctx, error):
        with open("cogs/data.json", 'r') as f:
            prefixes = json.load(f)
        pref = prefixes['servers'][str(ctx.guild.id)]['prefix']
        emb = discord.Embed(description=f':no_entry_sign: Неверный синтаксис!\nИспользуй {prefix}commands', color=discord.Colour.red())
        return emb

async def get_prefixes(ctx):
    prefix = pref.find_one({"GuildID": ctx.guild.id})['Prefix']
    return prefix

async def get_error(ctx, synt):
    pref = await get_prefixes(ctx)
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

async def get_ecoemoji(ctx):
    return ecoemoji.find_one({"GuildID": ctx.guild.id})['Emoji']

async def get_owners():
    if owners.count_documents({"MemberID": 263708575241601024}) == 0:
        owners.insert_one({"MemberID": 263708575241601024, "Owner": True})
    owns = []
    for own in owners.find({"Owner": True}):
        owns.append(own['MemberID'])
    return owns

async def get_data():
    with open('cogs/data.json', 'r') as f:
        return json.load(f)

async def get_time_now():
    return time.strftime("%d.%m.%Y в %H:%M")

async def get_money(ctx, member):
    return bal.find_one({"GuildID": ctx.guild.id, "MemberID": member.id})['Balance']

async def up_money(ctx, member, co):
    mon = await get_money(ctx, member)
    return bal.update_one({"GuildID": ctx.guild.id, "MemberID": member.id}, {"$set": {"Balance": mon+co}})

async def add_bal_user(ctx, member):
    return self.bal.insert_one({"GuildID": guild.id, "GuildName": guild.name, "MemberID": member.id, "MemberName": str(member), "Balance": 0})

async def hid_emb():
    return discord.Colour.from_rgb(47, 49, 54)

