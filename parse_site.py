from selenium import webdriver
from mongo import lastnews
import os


async def get_last_post():
    url = f'https://vk.com/ia_panorama'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920,5000")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    browser.get(url)

    i = 0
    for res in browser.find_elements_by_class_name("wall_text"): 
        i += 1
        if i == 3:
            for down in browser.find_elements_by_class_name("replies"):
                i += 1
                if i == 6:
                    checktext = res.text
                    checklast = lastnews.find_one({"Check": "PanoramaVK"})['LastPost']
                    if str(checklast) != str(checktext) or checklast is None:
                        lastnews.update_one({"Check": "PanoramaVK"}, {"$set": {"LastPost": str(checktext)}})
                        res.screenshot('resulttest/lastpostpanorama.png')
                        return True
                    else:
                        return False
    browser.close()