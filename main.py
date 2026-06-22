import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# প্রতি ৬০ সেকেন্ড পরপর সিগন্যাল পাঠানোর লজিক
async def send_signal(context: ContextTypes.DEFAULT_TYPE):
    # আপনার Quotex সিগন্যাল এখানে লিখুন
    message = "🎯 সিগন্যাল: AUD/CAD OTC\n📈 ট্রেন্ড: BUY (UP)\n⏰ সময়: ১ মিনিট"
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ বট এখন প্রতি ১ মিনিট অন্তর সিগন্যাল পাঠাবে!')
    # জবের মাধ্যমে লুপ চালু করা
    context.job_queue.run_repeating(send_signal, interval=60, first=5, chat_id=update.effective_chat.id)

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    
    print("Bot is running...")
    application.run_polling()
