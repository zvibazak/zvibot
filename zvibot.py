argparser = cap.ArgParser(default_config_files=['keys.yml'])
argparser.add('--bot_chatID', env_var='BOT_CHAT_ID')
argparser.add('--bot_token', env_var='BOT_TOKEN')

def telegram_bot_sendtext(bot_message):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage"
    send_text = url + '?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    r = requests.get(send_text)
    print(r.status_code, r.reason, r.content)
telegram_bot_sendtext("test")
