import telebot
from telebot import types
from app.db import *

TOKEN = '1018909192:AAFCCirDJ72yQyTijRNksDxZ0LzeWvSKdik'
bot = telebot.TeleBot(TOKEN)


date_regex = r"^(20|21)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
date_m_regex = r"^(20|21)[0-9]{2}-(0[1-9]|1[0-2])$"


@bot.message_handler(regexp=date_regex)
def task_1(message):
    chat_id = message.chat.id
    date = message.text
    msg = get_day_cancel(date)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(regexp=date_m_regex)
def task_2(message):
    chat_id = message.chat.id
    date_m = message.text
    msg = month_stat(date_m)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(content_types=['text'])
def recommendation(message):
    chat_id = message.chat.id
    msg = 'Error message!\nIt should be in forms given below:\nFOR TASK1: YYYY-MM-DD\nFOR TASK2: YYYY-MM'
    bot.send_message(chat_id, msg)
    return


if __name__ == "__main__":
    bot.polling(None)
