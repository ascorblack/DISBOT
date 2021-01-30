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


class Picture(commands.Cog):
    """Random picture from others sites"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["imgur"], help = 'img/imgur <tags>\nSearch on imgur.com')
    async def img(self, ctx, *, tag = None):
        if tag != None:
            ran = random.randint(1, 60)
            url = f'https://imgur.com/search/time?q={tag}'
            rs = requests.get(url)
            soup = BeautifulSoup(rs.content, 'lxml')
            a = []
            for img in soup.find_all('a', class_='image-list-link', height=None, href=True, limit=60):
                a.append(img['href'])
            sit = f'https://imgur.com{a[ran]}'
            await ctx.send(sit)
        else:
            emb = discord.Embed(title=f'{ctx.author}, пожалуйста, напиши тэг')
            await ctx.send(embed=emb)
    @commands.command(help = 'r34 <tags>\nSearch on https://rule34.xxx/')
    @commands.is_nsfw()
    async def r34(self, ctx, *, tag):
        urls = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}'
        ros = requests.get(urls)
        soup = BeautifulSoup(ros.content, 'lxml')
        try:
            last = ''
            for page in soup.find_all('a', id=False, href=True, alt="last page"):
                last += f'{page["href"]}'
            pag = last.split('pid=')
            lpages = pag[1].strip()
            page = random.randint(1, int(lpages))
            url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={page}'
            rs = requests.get(url)
            soup = BeautifulSoup(rs.content, 'lxml')
            a = []
            for img in soup.find_all('a', id=True, href=True, limit=60):
                a.append(img['href'])
            num = len(a)
            ran = random.randint(1, num)
            sit = f'https://rule34.xxx/{a[ran]}'
            try:
                root = requests.get(sit)
                soup = BeautifulSoup(root.content, 'lxml')
                out = []
                for imag in soup.find_all('img', alt=True, src=True, id=True):
                    out.append(imag['src'])
                await ctx.send(f'{int(lpages)} страниц найдено!\n{out[0]}')
            except:
                root = requests.get(sit)
                soup = BeautifulSoup(root.content, 'lxml')
                out = []
                for imag in soup.find_all('source', src=True, type=True):
                    out.append(imag['src'])
                await ctx.send(f'{int(lpages)} страниц найдено!\n{out[0]}')
        except:
            url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}'
            rs = requests.get(url)
            soup = BeautifulSoup(rs.content, 'lxml')
            a = []
            for img in soup.find_all('a', id=True, href=True):
                a.append(img['href'])
            num = len(a)
            ran = random.randint(1, num)
            sit = f'https://rule34.xxx/{a[ran]}'
            try:
                root = requests.get(sit)
                soup = BeautifulSoup(root.content, 'lxml')
                out = []
                for imag in soup.find_all('img', alt=True, src=True, id=True):
                    out.append(imag['src'])
                await ctx.send(out[0])
            except:
                root = requests.get(sit)
                soup = BeautifulSoup(root.content, 'lxml')
                out = []
                for imag in soup.find_all('source', src=True, type=True):
                    out.append(imag['src'])
                await ctx.send(out[0])
    @commands.command(help = 'rbomb <tags>\nSearch on https://rule34.xxx/ and output 5 results')
    @commands.is_nsfw()
    async def rbomb(self, ctx, *, tag = None):
        check = []
        output = ''
        i = 0
        count = 5
        urls = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}'
        ros = requests.get(urls)
        soup = BeautifulSoup(ros.content, 'lxml')
        try:
            last = ''
            for page in soup.find_all('a', id=False, href=True, alt="last page"):
                last += f'{page["href"]}'
            pag = last.split('pid=')
            lpages = pag[1].strip()
            page = random.randint(1, int(lpages))
            url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={page}'
            rs = requests.get(url)
            soup = BeautifulSoup(rs.content, 'lxml')
            a = []
            for img in soup.find_all('a', id=True, href=True, limit=60):
                a.append(img['href'])
            num = len(a) - 1
            while i < count:
                ran = random.randint(1, num)
                sit = f'https://rule34.xxx/{a[ran]}'
                try:
                    root = requests.get(sit)
                    soup = BeautifulSoup(root.content, 'lxml')
                    out = []
                    for imag in soup.find_all('img', alt=True, src=True, id=True):
                        out.append(imag['src'])
                    if i > 0:
                        if not str(out[0]) in check:
                            check.append(str(out[0]))
                            output += f'{out[0]}\n'
                            i += 1
                        else:
                            pass
                    else:
                        output += f'{out[0]}\n'
                        check.append(str(out[0]))
                        i += 1
                except:
                    root = requests.get(sit)
                    soup = BeautifulSoup(root.content, 'lxml')
                    out = []
                    for imag in soup.find_all('source', src=True, type=True):
                        out.append(imag['src'])
                    if i > 0:
                        if not str(out[0]) in check:
                            check.append(str(out[0]))
                            output += f'{out[0]}\n'
                            i += 1
                        else:
                            pass
                    else:
                        output += f'{out[0]}\n'
                        check.append(str(out[0]))
                        i += 1
            await ctx.send(output)
        except:
            url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}'
            rs = requests.get(url)
            soup = BeautifulSoup(rs.content, 'lxml')
            a = []
            for img in soup.find_all('a', id=True, href=True):
                a.append(img['href'])
            num = len(a) - 1
            h = count
            if num <= count:
                h = num
            while i < h:
                ran = random.randint(1, num)
                sit = f'https://rule34.xxx/{a[ran]}'
                try:
                    root = requests.get(sit)
                    soup = BeautifulSoup(root.content, 'lxml')
                    out = []
                    for imag in soup.find_all('img', alt=True, src=True, id=True):
                        out.append(imag['src'])
                    if i > 0:
                        if not str(out[0]) in check:
                            check.append(str(out[0]))
                            output += f'{out[0]}\n'
                            i += 1
                        else:
                            pass
                    else:
                        output += f'{out[0]}\n'
                        check.append(str(out[0]))
                        i += 1
                except:
                    root = requests.get(sit)
                    soup = BeautifulSoup(root.content, 'lxml')
                    out = []
                    for imag in soup.find_all('source', src=True, type=True):
                        out.append(imag['src'])
                    if i > 0:
                        if not str(out[0]) in check:
                            check.append(str(out[0]))
                            output += f'{out[0]}\n'
                            i += 1
                        else:
                            pass
                    else:
                        output += f'{out[0]}\n'
                        check.append(str(out[0]))
                        i += 1
            await ctx.send(output)


    @rbomb.error
    async def rbomb_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            emb = discord.Embed(description=f':no_entry_sign: При поиске произошла ошибка!\nПопробуйте ввести другой тэг.', color = discord.Colour.red())
            await ctx.send(embed=emb)
    @r34.error
    async def r34_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            emb = discord.Embed(description=f':no_entry_sign: При поиске произошла ошибка!\nПопробуйте ввести другой тэг.', color = discord.Colour.red())
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Picture(bot))