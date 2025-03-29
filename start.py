import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from states import GET_TABLE_EROR

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['клешня не зажимает'], ['кнопка залипла'], [' джойстик не работает'], ['оплатил картой деньги списали и игру не дали'], ['монету взял а игру не начала'], ['взял купюру а игру не начал'], ['застряла игрушка'], ['клешня не открывается'],['нет в этом списке']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"добро пожаловать {update.effective_user.first_name}\n\nчто случилось?",
        reply_markup=markup,
    )
    
    return GET_TABLE_EROR