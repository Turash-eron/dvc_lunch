import os
import telebot
from flask import Flask, request

TOKEN = '5101765622:AAHfaWFO3a7gS-kE4GEn6LLnHyF6eKAJdI0'
APP_URL = 'https://git.heroku.com/lunchbotdvc.git/' + TOKEN
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")


@server.route(f"/{TOKEN}", methods=["POST"])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
