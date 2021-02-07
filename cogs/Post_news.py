import json
import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from mongo import *
from parse_site import *


class Post_news(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.newschan = newschan
        self.lock = asyncio.Lock()
        self.reg_loop.start()

    async def loop_post_news(self):
        print("Начал")
        for guild in self.bot.guilds:
            check = self.newschan.find_one({"GuildID": guild.id})["ChannelID"]
            if check != 0:
                channel = self.bot.get_channel(check)
                last_new = await parse_panorama()
                for news in last_new:
                    await channel.send(news)

    @tasks.loop(seconds=600)
    async def reg_loop(self):
        async with self.lock:
            await self.loop_post_news()


def setup(bot):
    bot.add_cog(Post_news(bot))
