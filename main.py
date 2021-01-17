from config import settings
import json
import random
import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, HelpCommand, Command
import time
from funcs import *

#Functions
def get_prefix(client, ctx):
    with open("cogs/data.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes['servers'][str(ctx.guild.id)]['prefix']
def get_ownerses():
    with open("cogs/data.json", 'r') as f:
        owner = json.load(f)
    ownerses = []
    for own in owner['owners']:
        ownerses.append(own)
    return ownerses


bot = commands.Bot(command_prefix=get_prefix, owner_ids = get_ownerses(), intents = discord.Intents.all())
bot.owner_ids = get_ownerses()
bot.queue = []

#Events
@bot.event
async def on_ready():
    print('Bot is connected!')
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"suggestions"))
@bot.event
async def on_guild_join(guild):
    with open("cogs/data.json", 'r') as f:
        pref = json.load(f)
    if not 'servers' in pref:
        pref['servers'] = {}
    pref['servers'][str(guild.id)] = {}
    pref['servers'][str(guild.id)]['prefix'] = '-'
    pref['servers'][str(guild.id)]['ecoemoji'] = ':dollar:'
    pref['servers'][str(guild.id)]['money'] = {}
    pref['servers'][str(guild.id)]['shop'] = {}
    pref['servers'][str(guild.id)]['shop']['Role'] = {}
    pref['servers'][str(guild.id)]['shop']['item'] = {}
    pref['servers'][str(guild.id)]['inv'] = {}
    with open("cogs/data.json", 'w') as f:
        json.dump(pref, f, indent=4)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** You are missing Administrator permission to run this command.", color=discord.Colour.red())
        await ctx.send(embed=emb)
    if isinstance(error, commands.NotOwner):
        emb = discord.Embed(description=f":no_entry_sign: **{ctx.author}** You do not owner this bot!", color=discord.Colour.red())
        await ctx.send(embed=emb)
    # if isinstance(error, commands.MissingRequiredArgument):
    #     emb = await get_er_mis(ctx, error)
    #     await ctx.send(embed=emb)

#Embed help
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(title=f'Help', color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += f'{page}\n'
        e.set_footer(text='My commands', icon_url=bot.user.avatar_url)
        await destination.send(embed=e)
bot.help_command = MyHelpCommand()


#Load Cogs
fil = ''
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "funcs.py":
        bot.load_extension(f'cogs.{filename[:-3]}')
        fil += f'{filename[:-3]} '
print(fil)


bot.run(settings['TOKEN'])