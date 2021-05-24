import ephem
import csv
import logging
from typing import Text
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL,
    #'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, Юзер')
    #print(update)

    
def def_name(update, context):
    name_planet = update.message.text.split()
    date_now = datetime.now().strftime('%Y/%m/%d')
    #for i in enumerate(name_planet):
    cc =name_planet [1]
    user_planet = getattr(ephem, cc)
    constellation = ephem.constellation(user_planet(date_now))    
    #zvz = getattr(ephem.constellation,'{cc}')   
    update.message.reply_text(constellation)
    print(constellation)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def def_word (update,context):
    word_text = update.message.text.split()    
    word_text.remove('/wordcount')
    print(word_text)
    if (len(word_text) == 0):
        update.message.reply_text('Вы ввели пустое предложение')
    elif (word_text == ''):
        update.message.reply_text('Вы ввели пробел')
    else:
        wt = len(word_text)
        update.message.reply_text(f'{wt} слова')

def def_moon(update,context):
    date_t = datetime.now().strftime('%Y/%m/%d')
    mn = ephem.next_full_moon(date_t)
    update.message.reply_text(mn)


def def_city(update,context):
    with open("goroda.csv", encoding='utf-8') as r_file:
        reader_object = csv.DictReader(r_file, delimiter = ",")
    print(reader_object)
    ct = ['Москва', 'Новосибирск', 'Абакан', 'Красноярск']
    ct_text = update.message.text.split()
    ct_text.remove('/cities')
    for i in ct:
        if i == ct_text[0]:
            symbol = i[len(i)-1]
            ct.remove(i)
            for j in ct:
                symbol_up = symbol.upper()
                if j[0] == symbol_up:
                    update.message.reply_text(f'{j}')
                    symbol_up_s = j[len(j)-1]
                    ct.remove(j)
                    update.message.reply_text(f'Тебе на {symbol_up_s}')  





def main ():
    mybot=Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", def_name))
    dp.add_handler(CommandHandler("wordcount", def_word))
    dp.add_handler(CommandHandler("moon", def_moon))
    dp.add_handler(CommandHandler("cities", def_city))
    logging.info('Bot Startoval')
    mybot.start_polling()
    mybot.idle()


main()    