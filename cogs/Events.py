from config import settings
import json
import random
import discord
import os
from glob import glob
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or, command, has_permissions, HelpCommand, Command, Context
import time
from funcs import *
from db import db



class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ready = False
        self.guild = None
       #  self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", ((guild.id,) for guild in self.bot.guilds))
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    mem = db.field("SELECT MemberID FROM balance WHERE GuildID = ? AND MemberID = ?", guild.id, member.id)
                    if member.id == mem:
                        pass
                    elif member.id != mem:
                        db.execute("INSERT OR IGNORE INTO balance (GuildID, GuildName, MemberName, MemberID) VALUES (?,?,?,?)", guild.id, guild.name, str(member), member.id)
        db.commit() 


    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')
        for guild in self.bot.guilds:
            if not member.bot:
                mem = db.field("SELECT MemberID FROM balance WHERE GuildID = ? AND MemberID = ?", guild.id, member.id)
                if member.id == mem:
                    pass
                elif mem == None or member.id != mem:
                    db.execute("INSERT OR IGNORE INTO balance (GuildID, GuildName, MemberName, MemberID) VALUES (?,?,?,?)", guild.id, guild.name, str(member), member.id)
        db.commit()

    
    @commands.Cog.listener()
    async def on_member_leave(self, member):
        print(f'{member} left!')


    @commands.Cog.listener()
    async def on_connect(self):
        print('Bot is connected!')  

    @commands.Cog.listener()    
    async def on_ready(self):
        self.update_db()
        while True:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"suggestions")) 
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("cogs/data.json", 'r') as f:
            pref = json.load(f)
        if not 'servers' in pref:
            pref['servers'] = {}
        pref['servers'][str(guild.id)] = {}
        pref['servers'][str(guild.id)]['ecoemoji'] = ':dollar:'
        pref['servers'][str(guild.id)]['shop'] = {}
        pref['servers'][str(guild.id)]['shop']['Role'] = {}
        pref['servers'][str(guild.id)]['shop']['item'] = {}
        pref['servers'][str(guild.id)]['inv'] = {}
        for member in guild.members:
            if not member.bot:
                if not pref['servers'][str(guild.id)]['inv'][str(member.id)]:
                    pref['servers'][str(guild.id)]['inv'][str(member.id)] = {}
        with open("cogs/data.json", 'w') as f:
            json.dump(pref, f, indent=4)
        db.execute("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", guild.id)
        for member in guild.members:
            if not member.bot:
                db.execute("INSERT OR IGNORE INTO balance (GuildID, MemberName, MemberID) VALUES (?,?,?)", guild.id, str(member), member.id)
        db.commit()

    #async def on_command_error(self, ctx, error):
    #    if isinstance(error, commands.MissingPermissions):
    #        emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** You are missing Administrator permission to run this command.", color=discord.Colour.red())
    #        await ctx.send(embed=emb)
    #    if isinstance(error, commands.NotOwner):
    #        emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** You do not owner this bot!", color=discord.Colour.red())
    #        await ctx.send(embed=emb)
    #    # if isinstance(error, commands.MissingRequiredArgument):
    #    #     emb = await get_er_mis(ctx, error)
    #    #     await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Events(bot))