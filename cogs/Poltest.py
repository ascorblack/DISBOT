import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from funcs import *
import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Poltest(commands.Cog):
    """Political Test '9Axes'"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poltest(self, ctx):
        options = webdriver.ChromeOptions()
        # options.headless = True
        options.binary_location = 'GOOGLE_CHROME_BIN'
        browser = webdriver.Chrome(options=options)
        browser.get("https://9axes.github.io/ru/quiz.html")

        i = 0
        e = 0
        while i < 1:
            num = browser.find_element_by_id("question-number").text
            quest = browser.find_element_by_id("question-text").text
            emb = discord.Embed(description=f'**{num}**\n```{quest}```')
            if i > 0:
                await msg.edit(embed=emb)
            else:
                msg = await ctx.send(embed=emb)
            emojis = ["✅", "👍", "👊", "👎", "❌"]
            while e < len(emojis):
                emoji = emojis[e].strip()
                await msg.add_reaction(emoji)
                e += 1

            def check(reaction, user):
                return user != self.bot.user and str(reaction.emoji) in emojis
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=240, check=check)
                if str(reaction.emoji) == "✅":
                    button = browser.find_element_by_xpath('//*[@onclick="next_question( 2)"]')
                    ActionChains(browser).click(button).perform()
                if str(reaction.emoji) == "👍":
                    button = browser.find_element_by_xpath('//*[@onclick="next_question( 1)"]')
                    ActionChains(browser).click(button).perform()
                if str(reaction.emoji) == "👊":
                    button = browser.find_element_by_xpath('//*[@onclick="next_question( 0)"]')
                    ActionChains(browser).click(button).perform()
                if str(reaction.emoji) == "👎":
                    button = browser.find_element_by_xpath('//*[@onclick="next_question(-1)"]')
                    ActionChains(browser).click(button).perform()
                if str(reaction.emoji) == "❌":
                    button = browser.find_element_by_xpath('//*[@onclick="next_question(-2)"]')
                    ActionChains(browser).click(button).perform()
            except asyncio.TimeoutError:
                await ctx.send("Время на ответ истекло!")
                exit
            i += 1
        result = browser.find_element_by_id("banner").screenshot_as_png
        await ctx.send(file=discord.File(result))
        browser.quit()


def setup(bot):
    bot.add_cog(Poltest(bot))