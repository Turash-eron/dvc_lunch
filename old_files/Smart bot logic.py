#  Importing libs
from random import randint
import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import aioschedule

#  Define the list of recipients by Telegram chat id
chats = [450689077, 450689077]
restaurants = ['Обед-Буфет',
               'Чихо',
               'Корнер с шурмой',
               'Дегустатор',
               'Советская столовка',
               'Прайм-биф',
               'Индийская точка']

#  Basic and global constants constants
TOKEN = '00000000000000000000000000000000000000000'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
lunch_flag = 0

###############################################################
#  ***** ***** ***** BOT LOGIC DESCRIPTION ***** ***** *****  #

async def lunch_print():
    await bot.send_message(450689077, "Lunch time! Сегодня на очереди: " + str(restaurants[randint(0, len(restaurants)-1)]) + "! Приятного!")
    #await bot.send_message(-596089645, "Lunch time! Приятного!")
#  Function --- Schedules a timer to notify about lunch 
async def scheduler():
    aioschedule.every().day.at("1:10").do(lunch_print)
        
    #  Completing the precess until there are no more in queue
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

#  Handler for /timer function
@dp.message_handler(commands=['timer'])
async def lunch_status_check(message: types.Message):
    global lunch_flag
    if lunch_flag == 0:
        for idnum in chats:
            await bot.send_message(idnum, "Бот включен. Сегодня про обед вы не забудете!")
            print('nen')
        lunch_flag = 1
        asyncio.create_task(scheduler())
    elif lunch_flag == 1:
        for idnum in chats:
            await bot.send_message(idnum, "Так, братан, я включен, не мороси...")


#  Script identification
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
