from config import settings
import json
import random
import discord
import os
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
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
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)


    def update_db(self):
        for guild in self.bot.guilds:
            welch = db.field("SELECT GuildID FROM welchannel WHERE GuildID = ?", guild.id)
            if welch == None:
                db.execute("INSERT OR IGNORE INTO welchannel (GuildID) VALUES (?)", guild.id)
            exlch = db.field("SELECT GuildID FROM exitchannel WHERE GuildID = ?", guild.id)
            if exlch == None:
                db.execute("INSERT OR IGNORE INTO exitchannel (GuildID) VALUES (?)", guild.id)
            pref = db.field("SELECT GuildID FROM Prefixes WHERE GuildID = ?", guild.id)
            if pref == None or pref != guild.id:
                db.execute("INSERT INTO Prefixes (GuildID, Prefix) VALUES (?,?)", guild.id, "-")
            for member in guild.members:
                if not member.bot:
                    guild = member.guild
                    mem = db.field("SELECT MemberID FROM balance WHERE GuildID = ? AND MemberID = ?", guild.id, member.id)
                    if member.id == mem:
                        pass
                    elif member.id != mem:
                        db.execute("INSERT OR IGNORE INTO balance (GuildID, GuildName, MemberName, MemberID) VALUES (?,?,?,?)", guild.id, guild.name, str(member), member.id)
        db.commit() 


    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')
        guild = member.guild
        welchan = db.field("SELECT ChannelID FROM welchannel WHERE GuildID = ?", guild.id)
        if welchan != None:
            channel = self.bot.get_channel(welchan)
            msg = db.field("SELECT Message FROM welchannel WHERE ChannelID = ?", welchan)
            await channel.send(f'{member.mention} {msg}')
        if not member.bot:
            mem = db.field("SELECT MemberID FROM balance WHERE GuildID = ? AND MemberID = ?", guild.id, member.id)
            if mem == None or member.id != mem:
                db.execute("INSERT OR IGNORE INTO balance (GuildID, GuildName, MemberName, MemberID) VALUES (?,?,?,?)", guild.id, guild.name, str(member), member.id)
        db.commit()

    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} left!')
        guild = member.guild
        exchan = db.field("SELECT ChannelID FROM exitchannel WHERE GuildID = ?", guild.id)
        if exchan != None:
            channel = self.bot.get_channel(exchan)
            msg = db.field("SELECT Message FROM exitchannel WHERE ChannelID = ?", exchan)
            await channel.send(f'{member.mention} {msg}')

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
        if not pref['servers'][str(guild.id)]:
            pref['servers'][str(guild.id)] = {}
            pref['servers'][str(guild.id)]['ecoemoji'] = ':dollar:'
            pref['servers'][str(guild.id)]['shop'] = {}
            pref['servers'][str(guild.id)]['shop']['Role'] = {}
            pref['servers'][str(guild.id)]['shop']['item'] = {}
            pref['servers'][str(guild.id)]['inv'] = {}
            for member in guild.members:
                if not member.bot:
                    pref['servers'][str(guild.id)]['inv'][str(member.id)] = {}
        with open("cogs/data.json", 'w') as f:
            json.dump(pref, f, indent=4)
        db.execute("INSERT OR IGNORE INTO Prefixes (GuildID) VALUES (?)", guild.id)
        db.execute("INSERT OR IGNORE INTO welchannel (GuildID) VALUES (?)", guild.id)
        db.execute("INSERT OR IGNORE INTO exitchannel (GuildID) VALUES (?)", guild.id)
        for member in guild.members:
            if not member.bot:
                mcheck = db.field("SELECT MemberID FROM balance WHERE MemberID = ? AND GuildID = ?", member.id, guild.id)
                if mcheck == None:
                    db.execute("INSERT OR IGNORE INTO balance (GuildID, MemberName, MemberID) VALUES (?,?,?)", guild.id, str(member), member.id)
        db.commit()

        

def setup(bot):
    bot.add_cog(Events(bot))