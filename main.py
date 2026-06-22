import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

# অটোমেটিক সিগন্যাল লুপ
async def auto_signal_loop(context: ContextTypes.DEFAULT_TYPE):
    while True:
        # এখানে আপনার সিগন্যাল লজিক থাকবে
        await context.bot.send_message(chat_id=context.job.chat_id, text="🚀 সিগন্যাল: AUD/CAD OTC - BUY NOW!")
        await asyncio.sleep(60) # প্রতি ৬০ সেকেন্ড পর পর সিগন্যাল

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('বট সিগন্যাল দেওয়া শুরু করেছে!')
    # লুপটি চালু করা
    asyncio.create_task(auto_signal_loop(context))

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
