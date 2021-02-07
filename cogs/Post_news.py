import json
import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from mongo import *
from parse_site import get_last_post


class Post_news(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.newschan = newschan
        self.lock = asyncio.Lock()
        self.reg_loop.start()

    async def loop_post_news(self):
        last_new = await get_last_post()
        if last_new:
            print("TRUE")
            for guild in self.bot.guilds:
                check = self.newschan.find_one({"GuildID": guild.id})["ChannelID"]
                if check != 0:
                    channel = self.bot.get_channel(check)
                    file = discord.File(open('resulttest/lastpostpanorama.png', 'rb'))
                    await channel.send(file=file)

    @tasks.loop(seconds=30)
    async def reg_loop(self):
        async with self.lock:
            await self.loop_post_news()


def setup(bot):
    bot.add_cog(Post_news(bot))
