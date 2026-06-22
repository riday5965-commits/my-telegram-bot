import os
import logging
import ccxt
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

# মার্কেট ডাটা ও সিগন্যাল লজিক
async def check_quotex_signal(context: ContextTypes.DEFAULT_TYPE):
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        # Quotex-এর জন্য সিম্পল সিগন্যাল লজিক
        # এটি শুধু একটি উদাহরণ, আপনি আপনার স্ট্র্যাটেজি অনুযায়ী এটি পরিবর্তন করতে পারেন
        message = f"📊 *Quotex সিগন্যাল আপডেট*\n\n📈 পেয়ার: {symbol}\n💰 বর্তমান দাম: {price} USDT\n\n💡 ১ মিনিট পর দামের মুভমেন্ট লক্ষ্য রাখুন।"
        
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # প্রতি ১ মিনিট (৬০ সেকেন্ড) পর পর সিগন্যাল চেক করবে
    context.job_queue.run_repeating(check_quotex_signal, interval=60, first=5, chat_id=update.effective_chat.id)
    await update.message.reply_text('✅ বট ১ মিনিট অন্তর Quotex ট্রেডিং সিগন্যাল দেওয়া শুরু করেছে!')

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
