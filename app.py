import telebot
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()
token = os.getenv("token")

bot = telebot.TeleBot(token)

#decorator
@bot.message_handler(commands=['start','main','hello'])
def main(message):
    bot.send_message(message.chat.id, f'Privet, {message.from_user.first_name}')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<strong>Nastya</strong>', parse_mode='html')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://github.com/kruasanow')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'p':
        bot.send_message(message.chat.id, 'salam, trarb')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.first_name}')


bot.polling(non_stop=True)