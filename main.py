import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_market(context: ContextTypes.DEFAULT_TYPE):
    # মার্কেট চেকের লজিক এখানে লিখুন
    await context.bot.send_message(chat_id=context.job.chat_id, text="১ মিনিটের আপডেট: মার্কেট পরিস্থিতি স্বাভাবিক।")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(check_market, interval=60, first=5, chat_id=update.effective_chat.id)
    await update.message.reply_text('বট ১ মিনিট অন্তর আপডেট দেওয়া শুরু করেছে!')

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
