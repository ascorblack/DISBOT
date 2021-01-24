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
from db import db

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
    pref = db.field("SELECT Prefix FROM Prefixes WHERE GuildID = ?", ctx.guild.id)
    return pref

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
    with open("cogs/data.json", 'r') as f:
        emoji = json.load(f)
    ID = await get_guild_id(ctx)
    emoji = emoji['servers'][ID]['ecoemoji']
    return emoji

async def get_owners():
    with open("cogs/data.json", 'r') as f:
        owner = json.load(f)
    ownerses = []
    for own in owner['owners']:
        ownerses.append(own)
    return ownerses

async def get_data():
    with open('cogs/data.json', 'r') as f:
        return json.load(f)

async def get_time_now():
    return time.strftime("%d.%m.%Y в %H:%M")

async def get_money(ctx, member):
    return db.field("SELECT Money FROM balance WHERE MemberID = ? AND GuildID = ?", member.id, ctx.guild.id)

async def up_money(ctx, member, co):
    ID = await get_guild_id(ctx)
    money = db.field("SELECT Money FROM balance WHERE MemberID = ? AND GuildID = ?", member.id, ID)
    return db.execute("UPDATE balance SET Money = ? WHERE MemberID = ? AND GuildID = ?", money+co, member.id, ID)

async def add_bal_user(ctx, member):
    return db.execute("INSERT OR IGNORE INTO balance (GuildID, GuildName, MemberName, MemberID) VALUES (?,?,?,?)", ctx.guild.id, ctx.guild.name, member.name, member.id)