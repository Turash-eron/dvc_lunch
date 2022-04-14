#  Importing libs
import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from aiogram.methods import SendPoll
import asyncio
import aioschedule
from random import randint, sample

#  Getting constants from Heroku environment 
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

#  Webhook setting and paths 
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

#  Webservers settings (port definition)
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

#  Defining additional variables 
lunch_flag = 0
chats = [450689077, -596089645]
restaurants = ['Обед-Буфет',
               'Чихо',
               'Корнер с шурмой',
               'Дегустатор',
               'Советская столовка',
               'Прайм-биф',
               'Индийская точка',
               'Meat&Fish',
               'Дальний Дегустатор',
               'Underground']

#  STARTUP - Standard operations <<<---------------------
async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

#  SHUTDOWN - Standard operations -------------------->>>
async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    

###############################################################
#  ***** ***** ***** BOT LOGIC DESCRIPTION ***** ***** *****  #

#  Basic lunch message
async def lunch_print():
    await bot.send_message(-596089645, "Lunch time! Сегодня на очереди: " + str(restaurants[randint(0, len(restaurants)-1)]) + "! Приятного!")
    await bot.send_poll(chat_id=-596089645,
                        question='Куда идем?',
                        options=random.sample(restaurants, 3),
                        type='regular',
                        is_anonymous=False)

#  Function - schedules a given task
async def scheduler():
    aioschedule.every().day.at("10:00").do(lunch_print)
        
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
            await bot.send_message(idnum, "you suck...")

            
@dp.message_handler(commands=['change'])
async def lunch_status_check(message: types.Message):
    await bot.send_message(-596089645, "Ок, как насчет: " + str(restaurants[randint(0, len(restaurants)-1)]) + "? М-м-м?...")

###############################################################
###############################################################
    
#  Script starter 
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT)
