from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
from mongo import *
from parse_site import get_last_post_panorama_vk, get_last_post_meduza_io
from datetime import datetime


class Post_news(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.newschan = newschan
        self.lock = asyncio.Lock()
        self.reg_loop.start()

    async def loop_post_news_panoramavk(self):
        last_new = await get_last_post_panorama_vk()
        if last_new:
            for guild in self.bot.guilds:
                check = self.newschan.find_one({"GuildID": guild.id})["ChannelID"]
                if check != 0:
                    channel = self.bot.get_channel(check)
                    if len(last_new) == 4:
                        emb = discord.Embed(title=f"Новость с сайта: {last_new[0]}",
                                            description=f'{last_new[1]}\n\nПродолжение здесь: {last_new[2]}',
                                            color=discord.Colour.blue(), timestamp=datetime.utcnow())
                        emb.set_image(url=last_new[3])
                        await channel.send(embed=emb)
                    else:
                        if len(last_new[1]) > 1:
                            photos = last_new[1]
                            await channel.send(f'**Новость взята из: https://vk.com/ia_panorama**'
                                               f'\n{last_new[0]}')
                            for link in photos:
                                await channel.send(f'{link}')
                        elif last_new[1] is None:
                            emb = discord.Embed(title=f"Новость взята из: https://vk.com/ia_panorama",
                                                description=f'{last_new[0]}', color=discord.Colour.blue(),
                                                timestamp=datetime.utcnow())
                            await channel.send(embed=emb)
                        else:
                            emb = discord.Embed(title=f"Новость взята из: https://vk.com/ia_panorama",
                                                description=f'{last_new[0]}', color=discord.Colour.blue(),
                                                timestamp=datetime.utcnow())
                            link_photo = last_new[1]
                            emb.set_image(url=link_photo[0])
                            await channel.send(embed=emb)

    async def loop_post_news_meduza(self):
        find = await get_last_post_meduza_io()
        if find:
            for guild in self.bot.guilds:
                check = self.newschan.find_one({"GuildID": guild.id})["ChannelID"]
                if check != 0:
                    channel = self.bot.get_channel(check)
                    await channel.send(find)

    @tasks.loop(seconds=800)
    async def reg_loop(self):
        async with self.lock:
            await self.loop_post_news_panoramavk()
            await self.loop_post_news_meduza()


def setup(bot):
    bot.add_cog(Post_news(bot))
