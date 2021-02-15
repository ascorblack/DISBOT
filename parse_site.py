import requests
import json
from mongo import lastnews
from bs4 import BeautifulSoup
import lxml


async def get_last_post_panorama_vk():
    access_token = 'fcfd642dfcfd642dfcfd642d22fc8b3d7fffcfdfcfd642d9cdf1a019291045e6b320489'
    v = '5.126'
    domain = 'ia_panorama'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    get_parse = requests.get(f"https://api.vk.com/method/wall.get?access_token={access_token}&v={v}&domain={domain}",
                             headers=headers)
    data = json.loads(get_parse.content)

    checklast = lastnews.find_one({"Check": "PanoramaVK"})['LastPost']
    try:
        publish = f'{data["response"]["items"][1]["attachments"][0]["link"]["caption"]}'
        text = f'{data["response"]["items"][1]["attachments"][0]["link"]["title"]}'
        news_link = f'{data["response"]["items"][1]["attachments"][0]["link"]["url"]}'
        photo_link = f'{data["response"]["items"][1]["attachments"][0]["link"]["photo"]["sizes"][0]["url"]}'
        if str(checklast) != str(text) or checklast is None:
            lastnews.update_one({"Check": "PanoramaVK"}, {"$set": {"LastPost": str(text)}})
            return publish, text, news_link, photo_link
        else:
            return False
    except:
        text = f'{data["response"]["items"][1]["text"]}'
        max_size = len(data["response"]["items"][1]["attachments"][0]["photo"]["sizes"]) - 1
        try:
            i = 0
            photo_link = []
            for qu in data["response"]["items"][1]["attachments"]:
                photo_link.append(
                    f'{data["response"]["items"][1]["attachments"][i]["photo"]["sizes"][max_size]["url"]}')
                i += 1
        except KeyError:
            photo_link = None
        if str(checklast) != str(text) or checklast is None:
            lastnews.update_one({"Check": "PanoramaVK"}, {"$set": {"LastPost": str(text)}})
            return text, photo_link
        else:
            return False


async def get_last_post_meduza_io():
    url = "https://meduza.io/rss2/all"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    api = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(api.text, "lxml")

    last_news_address = f'{soup.find("item").find("guid").text}'
    checklast = lastnews.find_one({"Check": "Meduza.io"})['LastPost']
    if str(checklast) != str(last_news_address):
        lastnews.update_one({"Check": "Meduza.io"}, {"$set": {"LastPost": str(last_news_address)}})

        return last_news_address
    else:
        return False
