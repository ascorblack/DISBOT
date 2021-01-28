from config import settings
import json
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or, command
from funcs import *
from mongo import *

def get_prefix(bot, message):
	prefix = pref.find_one({"GuildID": message.guild.id})['Prefix']
	return when_mentioned_or(prefix)(bot, message)
def get_ownerses():
    owns = []
    if owners.count_documents({"MemberID": 263708575241601024}) == 0:
        owners.insert_one({"MemberID": 263708575241601024, "Owner": True})
    for own in owners.find({"Owner": True}):
        owns.append(own['MemberID'])
    return owns

bot = commands.Bot(command_prefix=get_prefix, owner_ids = get_ownerses(), intents = discord.Intents.all())
bot.remove_command("help")
bot.queue = []


#Load Cogs
fil = ''
bot.coglist = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "funcs.py":
        bot.load_extension(f'cogs.{filename[:-3]}')
        fil += f'{filename[:-3]} '
        bot.coglist.append(filename[:-3])
if bot.coglist.count("Events") == 1:
    bot.coglist.remove('Events')
print(fil)

bot.run(settings['TOKEN'])