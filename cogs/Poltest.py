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
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import base64


class Poltest(commands.Cog):
    """Political Test '9Axes'"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poltest(self, ctx):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1440")
        browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        browser.get("https://9axes.github.io/ru/quiz.html")

        i = 0
        e = 0
        while i < 45:
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
                return user != self.bot.user and user.id == ctx.author.id and str(reaction.emoji) in emojis
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
        await msg.delete()
        browser.find_element_by_id('banner').screenshot('resulttest/result.png')
        emb = discord.Embed(title=f'{ctx.author} - ваш результат')
        file = discord.File(open('resulttest/result.png', 'rb'))
        await ctx.send(embed=emb, file=file)

def setup(bot):
    bot.add_cog(Poltest(bot))