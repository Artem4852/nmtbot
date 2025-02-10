import json, os, dotenv, time, re, pytz, string, random
import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    ApplicationBuilder,
    CallbackQueryHandler,
    filters
)
import dotenv



dotenv.load_dotenv()
token = os.getenv("TELEGRAM_API_TOKEN")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привіт! Я бот для підготовки до ЗНО/НМТ. Я задаватиму питання з історії України, а ти відповідай. Спробуєш? Натисни /question.",
        reply_markup=ReplyKeyboardMarkup([["/question"]], resize_keyboard=True)
    )

def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("question", question))
    # app.add_handler(CallbackQueryHandler(answer))

    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()