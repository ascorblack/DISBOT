from bs4 import BeautifulSoup
import requests
import lxml
import random
import asyncio
from selenium import webdriver
from mongo import lastnews
import os


async def get_last_news(tag):
    browser.get(f'https://panorama.pub/{tag}')

    html = browser.page_source
    print(html)
    try:
        soup = BeautifulSoup(html, 'lxml')

        block_search = soup.find('div', class_='news big-previews two-in-row')
        last_new = block_search.find('a', href=True, class_=True)
        url_last_new = f'https://panorama.pub{last_new["href"]}'
        print(url_last_new)
        return url_last_new
    except:
        return "error"


async def parse_panorama():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920,1440")
    global browser
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    list_news = []
    for tag in ['politics', 'society', 'science', 'economics']:
        lastnew = await get_last_news(tag)
        if lastnews.find_one({"Category": tag})['LastPost'] != lastnew:
            lastnews.update_one({"Category": tag}, {"$set": {"LastPost": lastnew}})
            list_news.append(str(lastnew))

    return list_news
