from config import settings
import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os

async def guild_id(ctx):
    guild = str(ctx.guild.id)
    return guild

async def test(ctx, msg):
    msg += " да"
    return msg