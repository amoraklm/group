import os
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Read token from env; fallback to hardcoded token (as requested)
TOKEN = os.getenv("BOT_TOKEN", "8171147106:AAFclL-w8m9xXJOOEQ-NAK0DlN7W4d_WEU0")

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! من ربات مدیریت گروه هستم 🤖")

# Welcome new members
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"خوش اومدی {member.first_name} 🌹")

# Filter messages containing links
def filter_links(update: Update, context: CallbackContext):
    text = update.message.text or ""
    if "http://" in text or "https://" in text or "t.me/" in text:
        try:
            update.message.delete()
        except Exception:
            pass
        update.message.reply_text("ارسال لینک مجاز نیست 🚫")

# /ban command (reply to a user's message)
def ban(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.kick_chat_member(update.message.chat.id, user_id)
            update.message.reply_text("کاربر بن شد ❌")
        except Exception as e:
            update.message.reply_text(f"بن ناموفق بود. خطا: {e}")
    else:
        update.message.reply_text("برای بن کردن باید روی پیام کاربر ریپلای کنید.")

# /mute command (reply to a user's message)
def mute(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.restrict_chat_member(
                update.message.chat.id,
                user_id,
                ChatPermissions(can_send_messages=False),
            )
            update.message.reply_text("کاربر میوت شد 🔇")
        except Exception as e:
            update.message.reply_text(f"میوت ناموفق بود. خطا: {e}")
    else:
        update.message.reply_text("برای میوت کردن باید روی پیام کاربر ریپلای کنید.")

def main():
    if not TOKEN or TOKEN.strip() == "":
        print("❌ BOT_TOKEN خالی است. لطفاً از .env یا متغیر محیطی استفاده کنید.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_links))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
