import json, os, dotenv, time, re, pytz, string, random
import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InputMediaPhoto
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

from api import Loader
from helper import load_user_data, save_user_data, letters, letters_uk_en, letters_en, letters_en_uk, fix_text, subjects_uk_en, merge_images


SUBJECT_ENTRY, SUBJECT_CHOICE = range(2)

dotenv.load_dotenv()
token = os.getenv("TELEGRAM_API_TOKEN")

async def start(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {}
    save_user_data(user_data)

    await update.message.reply_text(
        "Привіт! Я бот для підготовки до ЗНО/НМТ. Я можу задавати питання з багатьох предметів, а ти відповідай. Спробуєш? Спочатку, обери предмет. Натисни /subject.",
        reply_markup=ReplyKeyboardMarkup([["/subject"]], resize_keyboard=True, one_time_keyboard=True)
    )

async def question(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    user_data = load_user_data()
    section = user_data[user_id]["current_subject"]

    loader = Loader()
    question = loader.random_question(user_id, section)

    message = f"{question['question']}\n\n"
    for n, answer in enumerate(question["answers1"]):
        if "images" in answer:
            message += f"{letters[n]}) Зображення {n+1}\n"
        else:
            message += f"{letters[n]}) {answer}\n"

    message = fix_text(message)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(letters[n], callback_data=f"answer_{question['id']}:{section}:{n}") for n in range(len(question["answers1"]))]
    ])

    if question["img"]:
        await update.message.reply_photo(
            photo=question["img"]
        )
    if "images" in question["answers1"][0]:
        filename = merge_images(question["answers1"])
        await update.message.reply_photo(
            photo=filename
        )
    await update.message.reply_text(
        message,
        parse_mode="html",
        reply_markup=keyboard
    )

async def answer(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query.message.text)
    user_id = str(query.from_user.id)

    loader = Loader()
    callback_type, callback_data = query.data.split("_")
    if callback_type == "answer":
        question_id, section, answer_id = callback_data.split(":")
        answer_id = int(answer_id)
        question = loader.get_question(section, question_id)

        if question["result"] == letters_en[answer_id].lower():
            await query.answer("Вірно!")
        else:
            await query.answer("Невірно!")

        text = query.message.caption if query.message.photo else query.message.text
        text += f"\n\nПравильна відповідь: {letters_en_uk[question['result']].upper()}) {question['answers1'][letters_en.index(question['result'].upper())]}"
        if query.message.photo:
            await query.edit_message_caption(
            caption=text,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Показати пояснення", callback_data=f"explanation_{question_id}:{section}")]])
            )
        else:
            await query.edit_message_text(
            text, 
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Показати пояснення", callback_data=f"explanation_{question_id}:{section}")]])
            )
    elif callback_type == "explanation":
        question_id, section = callback_data.split(":")
        question = loader.get_question(section, question_id)
        text = query.message.caption if query.message.photo else query.message.text
        text += f"\n\n{question['explanation']}"
        text = fix_text(text)

        if query.message.photo:
            await query.edit_message_caption(
                caption=text,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Наступне питання", callback_data="next")]])
            )
        else:
            await query.edit_message_text(
                text, 
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Наступне питання", callback_data="next")]])
            )

async def subject_entry(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Оберіть предмет:",
        reply_markup=ReplyKeyboardMarkup([["Історія України", "Математика", "Українська Мова"], ["Фізика", "Хімія", "Біологія"], ["Географія", "Українська Література", "Англійська"]], resize_keyboard=True, one_time_keyboard=True)
    )

    return SUBJECT_CHOICE

async def subject_choice(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    user_data = load_user_data()
    subject = subjects_uk_en[update.message.text.lower().replace(" ", "_")]
    user_data[user_id]["current_subject"] = subject
    save_user_data(user_data)

    await update.message.reply_text(
        "Добре, тепер питання будуть з предмету " + update.message.text,
        reply_markup=ReplyKeyboardMarkup([["/question"]], resize_keyboard=True, one_time_keyboard=True)
    )

    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(token).build()

    subject_handler = ConversationHandler(
        entry_points=[CommandHandler("subject", subject_entry)],
        states={
            SUBJECT_CHOICE: [MessageHandler(filters.TEXT, subject_choice)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(subject_handler)
    app.add_handler(CallbackQueryHandler(answer))

    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()