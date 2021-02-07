from bs4 import BeautifulSoup
import requests
import lxml
import random
import asyncio
from selenium import webdriver
from mongo import lastnews


async def get_last_news(tag):
    browser.get(f'https://panorama.pub/{tag}')

    html = browser.page_source

    soup = BeautifulSoup(html, 'lxml')

    block_search = soup.find('div', class_='news big-previews two-in-row')
    last_new = block_search.find('a', href=True, class_=True)
    url_last_new = f'https://panorama.pub{last_new["href"]}'
    print(url_last_new)
    return url_last_new


async def parse_panorama():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("window-size=1920,1440")
    options.headless = True
    global browser
    browser = webdriver.Chrome(executable_path="C:/Users/sanch/Desktop/bot/selenium/path/chromedriver.exe",options=options)
    list_news = []
    for tag in ['politics', 'society', 'science', 'economics']:
        lastnew = await get_last_news(tag)
        if lastnews.find_one({"Category": tag})['LastPost'] != lastnew:
            lastnews.update_one({"Category": tag}, {"$set": {"LastPost": lastnew}})
            list_news.append(str(lastnew))

    return list_news
