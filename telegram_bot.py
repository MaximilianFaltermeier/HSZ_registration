import requests
import telegram
from privat_data import API_KEY, CHAT_ID


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def telegram_bot_sendphoto_by_url(url):
    bot = telegram.Bot(API_KEY)
    bot.send_photo(chat_id=CHAT_ID, photo=url)


telegram_bot_sendphoto_by_url('https://telegram.org/img/t_logo.png')
test = telegram_bot_sendtext("Testing Telegram bot")
print(test)
