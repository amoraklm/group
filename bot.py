from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# پاسخ به دستور /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! من آماده‌ام 🤖")

# پاسخ به پیام "Hello Robot"
def reply_hello(update: Update, context: CallbackContext):
    text = update.message.text
    if text.strip().lower() == "hello robot":
        update.message.reply_text("سلام علی")

def main():
    # توکن ربات شما
    TOKEN = ""

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_hello))

    # اجرا
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
