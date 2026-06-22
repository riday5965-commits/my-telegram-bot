import os
import ccxt
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get('TELEGRAM_TOKEN')

def start(update, context):
    update.message.reply_text('বটটি সচল হয়েছে!')

def main():
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
