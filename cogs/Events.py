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
from mongo import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ready = False
        self.guild = None
        self.pref = pref
        self.bal = bal
        self.owners = owners
        self.ecoemoji = ecoemoji
        self.welcch = welcch
        self.exitch = exitch
        self.newschan = newschan
        self.lastnews = lastnews


    def update_db(self):
        if self.owners.find({"MemberID": 263708575241601024}) is None:
            self.owners.insert_one({"MemberID": 263708575241601024, "Owner": True})
        for guild in self.bot.guilds:
            if self.ecoemoji.find_one({"GuildID": guild.id}) is None:
                self.ecoemoji.insert_one({"GuildID": guild.id, "Emoji": ":dollar:"})
            if self.pref.find_one({"GuildID": guild.id}) is None:
                self.pref.insert_one({"GuildID": guild.id, "Prefix": "-"})
            if self.welcch.count_documents({"GuildID": guild.id}) == 0:
                self.welcch.insert_one({"GuildID": guild.id, "Message": "приветствуем вас на нашем сервере!", "ChannelID": 0})
            if self.exitch.count_documents({"GuildID": guild.id}) == 0:
                self.exitch.insert_one({"GuildID": guild.id, "Message": "покинул наши ряды!", "ChannelID": 0})
            for member in guild.members:
                if not member.bot:
                    guild = member.guild
                    if self.bal.count_documents({"GuildID": guild.id, "MemberID": member.id}) == 0:
                        self.bal.insert_one({"GuildID": guild.id, "GuildName": guild.name, "MemberID": member.id, "MemberName": str(member), "Balance": 0})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if self.welcch.find_one({"GuildID": guild.id})['ChannelID'] != 0:
            welchan = self.welcch.find_one({"GuildID": guild.id})['ChannelID']
            channel = self.bot.get_channel(welchan)
            msg = self.welcch.find_one({"GuildID": guild.id, "ChannelID": welchan})['Message']
            await channel.send(f'{member.mention} {msg}')
        if not member.bot:
            if self.bal.count_documents({"GuildID": guild.id, "MemberID": member.id}) == 0:
                self.bal.insert_one({"GuildID": guild.id, "GuildName": guild.name, "MemberID": member.id, "MemberName": str(member), "Balance": 0})

    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if self.exitch.find_one({"GuildID": guild.id})['ChannelID'] != 0:
            exchan = self.exitch.find_one({"GuildID": guild.id})['ChannelID']
            channel = self.bot.get_channel(exchan)
            msg = self.exitch.find_one({"GuildID": guild.id, "ChannelID": exchan})['Message']
            await channel.send(f'**{member}** {msg}')

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
            pref['servers'][str(guild.id)]['shop'] = {}
            pref['servers'][str(guild.id)]['shop']['Role'] = {}
            pref['servers'][str(guild.id)]['shop']['item'] = {}
            pref['servers'][str(guild.id)]['inv'] = {}
            for member in guild.members:
                if not member.bot:
                    pref['servers'][str(guild.id)]['inv'][str(member.id)] = {}
        with open("cogs/data.json", 'w') as f:
            json.dump(pref, f, indent=4)
        if self.ecoemoji.find_one({"GuildID": guild.id}) == 0:
            self.ecoemoji.insert_one({"GuildID": guild.id, "Emoji": ":dollar:"})
        if self.welcch.count_documents({"GuildID": guild.id}) == 0:
            self.welcch.insert_one({"GuildID": guild.id, "Message": "приветствуем вас на нашем сервере!", "ChannelID": 0})
        if self.exitch.count_documents({"GuildID": guild.id}) == 0:
            self.exitch.insert_one({"GuildID": guild.id, "Message": "покинул наши ряды!", "ChannelID": 0})
        for member in guild.members:
            if not member.bot:
                if self.bal.count_documents({"GuildID": guild.id, "MemberID": member.id}) == 0:
                    self.bal.insert_one({"GuildID": guild.id, "GuildName": guild.name, "MemberID": member.id, "MemberName": str(member), "Balance": 0})

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** У тебя нет прав администратора для использования команды **{ctx.command}**", color=discord.Colour.red())
            await ctx.send(embed=emb)
        if isinstance(error, commands.NotOwner):
            emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** Тебя нет в списке Owners!", color=discord.Colour.red())
            await ctx.send(embed=emb)
        if isinstance(error, commands.NSFWChannelRequired):
            emb = discord.Embed(description=f':no_entry_sign: Канал **{ctx.channel}** не является NSFW!', color = discord.Colour.red())
            await ctx.send(embed=emb)
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            pref = await get_prefixes(ctx)
            emb = discord.Embed(description=f':no_entry_sign: Неверный синтаксис комманды!\n`{pref}{ctx.command.help}`', color = discord.Colour.red())
            await ctx.send(embed=emb)
        if isinstance(error, commands.CommandInvokeError):
            if not str(ctx.command) in ["emoinfo", "poltest", "r34", "rbomb"]:
                pref = await get_prefixes(ctx)
                emb = discord.Embed(description=f':no_entry_sign: Неверный синтаксис комманды!\n`{pref}{ctx.command.help}`', color = discord.Colour.red())
                await ctx.send(embed=emb)



        

def setup(bot):
    bot.add_cog(Events(bot))