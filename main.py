from config import settings
import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, HelpCommand, Command
import os
from funcs import *

def get_prefix(client, message):
    with open("cogs/data.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes['servers'][str(message.guild.id)]['prefix']

bot = commands.Bot(command_prefix=get_prefix)
# bot.eco_emoji =  get_ecoemoji(guild = commands.Context.guild)
bot.eco_emoji = ':dollar:'
# bot.remove_command('help')
bot.owner_ids = [263708575241601024]
queue = []


#Events
@bot.event
async def on_ready():
    print('Bot is connected!')
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"suggestions"))
@bot.event
async def on_guild_join(guild):
    with open("data.json", 'r') as f:
        pref = json.load(f)
    if not 'servers' in pref:
        pref['servers'] = {}
    pref['servers'][str(guild.id)] = {}
    pref['servers'][str(guild.id)]['prefix'] = '-'
    with open("data.json", 'w') as f:
        json.dump(pref, f, indent=4)
@bot.event
async def on_guild_remove(guild):
    with open("data.json", 'r') as f:
        pref = json.load(f)
    del pref['servers'][str(guild.id)]
    with open("data.json", 'w') as f:
        json.dump(pref, f, indent=4)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
    if isinstance(error, commands.NotOwner):
        emb = discord.Embed(description=f':no_entry_sign: Ты не Owner!', color=discord.Colour.red())
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