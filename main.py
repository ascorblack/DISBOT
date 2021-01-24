from config import settings
import json
import random
import discord
import os
from glob import glob
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or, command, has_permissions, HelpCommand, Command, Context
import time
from funcs import *
from db import db


def get_prefix(bot, message):
	prefix = db.field("SELECT Prefix FROM Prefixes WHERE GuildID = ?", message.guild.id)
	return when_mentioned_or(prefix)(bot, message)
def get_ownerses():
    with open("cogs/data.json", 'r') as f:
        owner = json.load(f)
    ownerses = []
    for own in owner['owners']:
        ownerses.append(own)
    return ownerses

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