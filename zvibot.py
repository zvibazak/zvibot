import requests
from facebook_scraper import get_posts
import io
from datetime import datetime, timedelta
import twint
import json
import os

try:
    from tg_tokens import bot_token, bot_chatID
except ImportError:
    bot_token = os.getenv('BOT_TOKEN').strip()
    bot_chatID = os.getenv('BOT_CHAT_ID').strip()    
    
#change to your page
#PAGES_NAMES = ['שבתשתיות-ביצוע-פרויקטים-בתחבורה-373566349461843','HanochDaum']
PAGES_NAMES = ['HanochDaum']

#Telegram APIs
def telegram_bot_sendtext(bot_message):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage"
    send_text = url + '?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    r = requests.get(send_text)
    print(r.status_code, r.reason, r.content)

def telegram_bot_sendImageRemoteFile(img_url,caption):
    url = "https://api.telegram.org/bot"+bot_token+"/sendPhoto"
    remote_image = requests.get(img_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    files = {'photo': photo}
    data = {'chat_id' : bot_chatID, "caption" : caption[:1024]}
    r = requests.post(url, files=files, data=data)
    if len(caption)>1024:
        telegram_bot_sendtext(caption[1024:])
    
    print(r.status_code, r.reason, r.content)

def telegram_bot_sendVideoRemoteFile(video_url,caption):
    url = "https://api.telegram.org/bot"+bot_token+"/sendVideo"
    remote_video = requests.get(video_url)
    video = io.BytesIO(remote_video.content)
    video.name = 'video.mp4'
    files = {'video': video}
    data = {'chat_id' : bot_chatID, "caption" : caption[:1024]}
    r = requests.post(url, files=files, data=data)
    if len(caption)>1024:
        telegram_bot_sendtext(caption[1024:])
    
    print(r.status_code, r.reason, r.content)

def get_my_posts():
    now = datetime.now()
    for page_name in PAGES_NAMES:
        for post in get_posts(page_name, pages=2):
            print(post)
            print(post['post_id'] +' ' + str(post['text']) + " image: " + str(post['image']))
            if post['time']<=now-timedelta(hours=1):
                print("already sent this post...")
                continue

            if post['video']:
                telegram_bot_sendVideoRemoteFile(post['video'],post['text'] + " \n\n " + str(post['time']))
            if post['image']:
                telegram_bot_sendImageRemoteFile(post['image'],post['text'] + " \n\n " + str(post['time']))
            elif post['images']:
                for image in post['images']:
                    telegram_bot_sendImageRemoteFile(image," \n\n " + str(post['time']))
            else:
                telegram_bot_sendtext(post['text'] + ' ' + str(post['time']))

if __name__ == "__main__":
    get_my_posts()
