import requests
import json
from mongo import lastnews

async def get_last_post():
    access_token = 'fcfd642dfcfd642dfcfd642d22fc8b3d7fffcfdfcfd642d9cdf1a019291045e6b320489'
    v = '5.126'
    domain = 'ia_panorama'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }


    get_parse = requests.get(f"https://api.vk.com/method/wall.get?access_token={access_token}&v={v}&domain={domain}", headers=headers)
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
        text = f'{data["response"]["items"][1]["text"]}\n\n'
        max_size = len(data["response"]["items"][1]["attachments"][0]["photo"]["sizes"]) - 1
        photo_link = f'{data["response"]["items"][1]["attachments"][0]["photo"]["sizes"][max_size]["url"]}'
        if str(checklast) != str(text) or checklast is None:
            lastnews.update_one({"Check": "PanoramaVK"}, {"$set": {"LastPost": str(text)}})
            return text, photo_link
        else:
            return False



