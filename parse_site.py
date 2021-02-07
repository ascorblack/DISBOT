from bs4 import BeautifulSoup
import requests
import lxml
from mongo import lastnews


async def get_last_news(tag):
    root = requests.get(f'https://panorama.pub/{tag}')
    soup = BeautifulSoup(root.content, 'lxml')

    block_search = soup.find('div', class_='news big-previews two-in-row')
    last_new = block_search.find('a', href=True, class_=True)
    url_last_new = f'https://panorama.pub{last_new["href"]}'
    return url_last_new


async def parse_panorama():
    list_news = []
    for tag in ['politics', 'society', 'science', 'economics']:
        lastnew = await get_last_news(tag)
        if lastnews.find_one({"Category": tag})['LastPost'] != lastnew:
            lastnews.update_one({"Category": tag}, {"$set": {"LastPost": lastnew}})
            list_news.append(str(lastnew))

    return list_news
