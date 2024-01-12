import random
import sqlite3
import os

import telebot
from telebot import types
from dotenv import load_dotenv

from stats import Stats
from settings import Settings
from language import languages

load_dotenv()
my_secret = os.getenv('TOKEN')
bot = telebot.TeleBot(my_secret)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('English', callback_data='eng')
    button2 = types.InlineKeyboardButton('Russian', callback_data='ru')
    markup.add(button1, button2)

    user_id = message.chat.id

    bot.send_message(user_id, 'Hello! | Привет!')
    bot.send_message(user_id, 'Choose the language '
                              '| Выбирете язык',
                     reply_markup=markup)

    conn = sqlite3.connect('DB_game.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS DB_game(user_id integer PRIMARY KEY, '
        'wins integer, defeats integer, draws integer)')
    conn.commit()


@bot.message_handler(commands=['language'])
def langs(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('English', callback_data='eng')
    button2 = types.InlineKeyboardButton('Russian', callback_data='ru')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, 'Choose the language '
                                      '| Выбирете язык',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['eng', 'ru'])
def callback_language(query):
    data = query.data
    user_id = query.message.chat.id
    setting = Settings(user_id, data)
    setting.save_language()
    setting.insert()
    lang = setting.select_language()
    bot.send_message(user_id, languages[lang]['Hello'])


@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.chat.id
    setting = Settings(user_id)
    lang = setting.select_language()

    st = Stats(user_id)
    wins, losses, draws = st.get_stats()
    stats_text = languages[lang]['stats'].format(wins=wins, losses=losses,
                                                 draws=draws)
    bot.send_message(user_id, stats_text)


@bot.message_handler(commands=['game'])
def game(message):
    user_id = message.chat.id
    setting = Settings(user_id)
    lang = setting.select_language()
    button_text = languages[lang]['button'].split()

    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(f'{button_text[0]}',
                                    callback_data='\u270A')

    b2 = types.InlineKeyboardButton(f'{button_text[1]}',
                                    callback_data='\U0000270C')

    b3 = types.InlineKeyboardButton(f'{button_text[2]}',
                                    callback_data='\U0000270B')

    markup.row(b1, b2, b3)
    bot.send_message(user_id, f'{button_text[3]}',
                     reply_markup=markup)


@bot.message_handler(commands=['questions'])
def questions(message):
    user_id = message.chat.id
    setting = Settings(user_id)
    lang = setting.select_language()
    questions_text = languages[lang]['questions']

    bot.send_message(user_id, f'{questions_text}')


@bot.callback_query_handler(
    func=lambda call: call.data in ['\u270A', '\U0000270B', '\U0000270C'])
def callback_game(query):
    user_id = query.message.chat.id
    setting = Settings(user_id)
    lang = setting.select_language()
    game_text = languages[lang]['main_game']

    choice = ['\u270A', '\U0000270B', '\U0000270C']
    random_choice = random.choice(choice)
    data = query.data
    st = Stats(user_id)
    if data == '\u270A':  # rock
        bot.send_message(user_id, '\u270A')

    elif data == '\U0000270C':  # scissors
        bot.send_message(user_id, game_text['Your move'])
        bot.send_message(user_id, '\U0000270C')

    elif data == '\U0000270B':  # paper
        bot.send_message(user_id, game_text['Your move'])
        bot.send_message(query.message.chat.id, '\U0000270B')

    if data == '\u270A' or data == '\U0000270C' or data == '\U0000270B':
        bot.send_message(user_id, game_text["Bot's move"])
        bot.send_message(user_id, f'{random_choice}')

    if data == random_choice:
        bot.send_message(user_id, game_text['draw'])
        st.update_draw()

    elif data == '\u270A':
        if random_choice == '\U0000270C':
            bot.send_message(user_id, game_text['win'])
            st.update_wins()

        else:
            bot.send_message(user_id, game_text['lose'])
            st.update_losses()

    elif data == '\U0000270C':
        if random_choice == '\U0000270B':
            bot.send_message(user_id, game_text['win'])
            st.update_wins()

        else:
            bot.send_message(user_id, game_text['lose'])
            st.update_losses()

    elif data == '\U0000270B':
        if random_choice == '\u270A':
            bot.send_message(user_id, game_text['win'])
            st.update_wins()
        else:
            bot.send_message(user_id, game_text['lose'])
            st.update_losses()

    game(query.message)


bot.polling(none_stop=True)
