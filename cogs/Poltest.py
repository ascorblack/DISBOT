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

    @commands.command(help = 'poltest \nПолитический тест 9Axes')
    async def poltest(self, ctx):
        emb = discord.Embed(description="**Версия теста**\n🅰️ — из 216 вопросов\n🅱️ — из 45 вопросов\n")
        emb.set_footer(text='Оригинал теста https://9axes.github.io/ru/')
        choice = await ctx.send(embed=emb)
        cho = ['🅰️', '🅱️']
        await choice.add_reaction(cho[0])
        await choice.add_reaction(cho[1])
        def check(reaction, user):
            return user != self.bot.user and str(reaction.emoji) in cho and user.id == ctx.author.id
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)
            await choice.delete()
            if str(reaction.emoji) == '🅰️':
                urlt = "https://9axes.github.io/ru/fullquiz.html"
            if str(reaction.emoji) == '🅱️':
                urlt = "https://9axes.github.io/ru/quiz.html"

            emb = discord.Embed(description="**Значение реакций**\n✅ — Полностью согласен\n🟩 — Скорее согласен\n🟨 — Нейтрально/Не уверен\n🟥 — Скорее не согласен\n❌ — Полностью не согласен\n⏪ — На прошлый вопрос\n⏹ — Покинуть сессию\n__НА КАЖДЫЙ ВОПРОС ОТВОДИТСЯ 5 МИНУТ__\n\n*Нажмите ▶️ для начала*")
            emb.set_footer(text='Оригинал теста https://9axes.github.io/ru/')
            rule = await ctx.send(embed=emb)
            start = '▶️'
            await rule.add_reaction(start)
            def check(reaction, user):
                return user != self.bot.user and str(reaction.emoji) == start and user.id == ctx.author.id
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
                await rule.delete()
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("window-size=1920,1440")
                browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                browser.get(urlt)

                i = 0
                e = 0
                finish = False
                while not finish:
                    try:
                        check = browser.find_element_by_id('banner')
                        await msg.delete()
                        browser.find_element_by_id('banner').screenshot('resulttest/result.png')
                        file = discord.File(open('resulttest/result.png', 'rb'))
                        await ctx.send(f'**{ctx.author.mention}** — ваш результат', file=file)
                        finish = True
                    except:
                        num = browser.find_element_by_id("question-number").text
                        quest = browser.find_element_by_id("question-text").text
                        emb = discord.Embed(description=f'**{num}**\n```{quest}```')
                        emb.set_footer(icon_url=self.bot.user.avatar_url, text='Код написан SCORPS#7927')
                        if i > 0:
                            await msg.edit(embed=emb)
                        else:
                            msg = await ctx.send(embed=emb)
                        emojis = ["✅", "🟩", "🟨", "🟥", "❌", "▪️", "⏪", "⏹"]
                        while e < len(emojis):
                            emoji = emojis[e].strip()
                            await msg.add_reaction(emoji)
                            e += 1

                        def check(reaction, user):
                            return user != self.bot.user and user.id == ctx.author.id and str(reaction.emoji) in emojis
                        try:
                            reaction, user = await self.bot.wait_for("reaction_add", timeout=300, check=check)
                            if str(reaction.emoji) == "✅":
                                await msg.remove_reaction(emoji = "✅", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="next_question( 2)"]')
                                ActionChains(browser).click(button).perform()
                            if str(reaction.emoji) == "🟩":
                                await msg.remove_reaction(emoji = "🟩", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="next_question( 1)"]')
                                ActionChains(browser).click(button).perform()
                            if str(reaction.emoji) == "🟨":
                                await msg.remove_reaction(emoji = "🟨", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="next_question( 0)"]')
                                ActionChains(browser).click(button).perform()
                            if str(reaction.emoji) == "🟥":
                                await msg.remove_reaction(emoji = "🟥", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="next_question(-1)"]')
                                ActionChains(browser).click(button).perform()
                            if str(reaction.emoji) == "❌":
                                await msg.remove_reaction(emoji = "❌", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="next_question(-2)"]')
                                ActionChains(browser).click(button).perform()
                            if str(reaction.emoji) == "⏪":
                                await msg.remove_reaction(emoji = "⏪", member = ctx.author)
                                button = browser.find_element_by_xpath('//*[@onclick="prev_question()"]')
                                check = button.is_displayed()
                                if check == True:
                                    ActionChains(browser).click(button).perform()
                                else:
                                    pass
                            if str(reaction.emoji) == "⏹":
                                browser.close()
                                await msg.delete()
                        except asyncio.TimeoutError:
                            emb.set_footer(text='Время ожидания превышено!')
                            await msg.edit(embed=emb)
                            browser.close()
                            break
                        i += 1
            except asyncio.TimeoutError:
                emb.set_footer(text='Время ожидания превышено!')
                await rule.edit(embed=emb)
        except asyncio.TimeoutError:
            emb.set_footer(text='Время ожидания превышено!')
            await choice.edit(embed=emb)


def setup(bot):
    bot.add_cog(Poltest(bot))