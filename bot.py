from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# دستور /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! من ربات مدیریت گروه هستم 🤖")

# خوشامدگویی به اعضای جدید
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"خوش اومدی {member.first_name} 🌹")

# فیلتر لینک‌ها (پاک کردن پیام‌های دارای لینک)
def filter_links(update: Update, context: CallbackContext):
    if "http://" in update.message.text or "https://" in update.message.text:
        update.message.delete()
        update.message.reply_text("ارسال لینک مجاز نیست 🚫")

# دستور /ban
def ban(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        context.bot.kick_chat_member(update.message.chat.id, user_id)
        update.message.reply_text("کاربر بن شد ❌")
    else:
        update.message.reply_text("برای بن کردن باید روی پیام کاربر ریپلای کنید.")

def main():
    # توکن ربات رو اینجا بذار
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_links))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
