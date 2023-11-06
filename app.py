import telebot
from telebot import types
from dotenv import load_dotenv
import os
import webbrowser
import sqlite3

load_dotenv()
token = os.getenv("token")

bot = telebot.TeleBot(token)
name = None

# buttons about message ----------------------------------------------------------------
@bot.message_handler(commands=['start'])
def start(message):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Regestration - NAME?')
    bot.register_next_step_handler(message, user_name)

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('go to hell')
    markup.row(btn1)
    btn2 = types.KeyboardButton('go to heaven')
    btn3 = types.KeyboardButton('go to earth')
    markup.row(btn2, btn3)

    # file = open('media/123.jpg', 'rb') # audio video emodji
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'Salam aleykum', reply_markup=markup)

    bot.register_next_step_handler(message, on_click)
# end buttons about message ------------------------------------------------------------
def on_click(message):
    if message.text == 'go to hell':
        bot.send_message(message.chat.id, 'website is opened')
    elif message.text == 'go to heaven':
        bot.send_message(message.chat.id, 'ya eblan')

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (name, pass) VALUES ('{name}', '{password}')")

    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('User list', callback_data='users'))
    bot.send_message(message.chat.id, 'User regestrated', reply_markup=markup)

    #bot.send_message(message.chat.id, 'Введите пароль')
    #bot.register_next_step_handler(message, user_pass)

@bot.callback_query_handler(func=lambda call: True)
def call(call):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")
    users = cur.fetchall()

    info = ''
    for i in users:
        info += f'Name: {i[1]}, password: {i[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

# text - decorator ---------------------------------------------------------------------
@bot.message_handler(commands=['main','hello'])
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
# end text - decorator -----------------------------------------------------------------

# file - decorator ---------------------------------------------------------------------
@bot.message_handler(content_types=['photo'])
def get_photo(message):

    # buttons about message - decorator ------------------------------------------------
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('go to hell', url='https://google.com')
    markup.row(btn1)

    btn2 = types.InlineKeyboardButton('go to heaven', callback_data='delete')
    btn3 = types.InlineKeyboardButton('go to earth', callback_data='edit') # обрабатывается декоратором
    markup.row(btn2, btn3)
    # markup.add(types.InlineKeyboardButton('go to heaven', callback_data='delete'))
    # markup.add(types.InlineKeyboardButton('go to earth', callback_data='site'))

    # end buttons about message - decorator ------------------------------------------------
    bot.reply_to(message, 'very good cock', reply_markup = markup)

# react buttom about message - decorator ------------------------------------------------
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('edited text', callback.message.chat.id, callback.message.message_id)
# end react buttom about message - decorator ------------------------------------------------

# permanent circle 
bot.polling(non_stop=True)