import os
import requests

bot_token = os.getenv('BOT_TOKEN').strip()
bot_chatID = os.getenv('BOT_CHAT_ID').strip()

def telegram_bot_sendtext(bot_message,bot_chatID,bot_token):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage"
    send_text = url + '?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    r = requests.get(send_text)
    print(r.status_code, r.reason, r.content)
telegram_bot_sendtext("test",bot_chatID,bot_token)
