#  Importing libs
import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
import asyncio
import aioschedule

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

#  STARTUP - Standard operations <<<---------------------
async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

#  SHUTDOWN - Standard operations -------------------->>>
async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    
    
async def lunch_print():
    await bot.send_message(450689077, "Lunch time! Приятного!")
    await bot.send_message(-596089645, "Lunch time! Приятного!")
#  Function --- Schedules a timer to notify about lunch 
async def scheduler():
    aioschedule.every().day.at("21:49").do(lunch_print)
        
    #  Completing the precess until there are no more in queue
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

#  1.0 Handler for /timer function    
@dp.message_handler(commands=['timer'])
#  1.1 Welcome message
#async def send_welcome(msg: types.Message):
    #await msg.reply_to_message('Я бот. Приятно познакомиться. Я буду напоминать вам про ланч!')'''
#  1.2 Schedule a task 
async def process_start_command(message: types.Message):
    asyncio.create_task(scheduler())  

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
    
            #async def process_start_command(message: types.Message):
            #await bot.send_message(message.from_user.id, "test message")
            
                    # Sending messages by ID
        #async def process_start_command(message: types.Message):
            #await bot.send_message(450689077, "Lunch time!")
         #async def process_start_command(message: types.Message):
           # await bot.send_message(-596089645, "Lunch time")
