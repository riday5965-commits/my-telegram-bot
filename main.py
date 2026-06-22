import os
import ccxt
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text('বটটি সচল হয়েছে!')

def main():
    token = os.environ.get('TELEGRAM_TOKEN')
    # নতুন ভার্সনের জন্য use_context সরিয়ে ফেলেছি
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
