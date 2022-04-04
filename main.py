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

#  Function for lunch printing
async def lunch_print():
    print("It's noon!")
    
#  Function --- Schedule lunch 
async def scheduler():
    aioschedule.every().day.at("11:20").do(lunch_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

#  Message handler --- Receives input from client and starts scheduler 
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    asyncio.create_task(scheduler())

    
#async def on_startup(_):
#    asyncio.create_task(scheduler())


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
