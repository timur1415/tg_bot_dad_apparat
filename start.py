from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)

from states import GET_TABLE_EROR, TOYS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['клешня не закрывается'], ['кнопка залипла'], ['джойстик не работает'], ['после оплаты картой игра не началась'], ['после оплаты монетой игра не началась'], ['после оплаты купюрой игра не началась'], ['застряла игрушка'], ['клешня не открывается'],['нет в этом списке']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"добро пожаловать {update.effective_user.first_name},что случилось?",
        reply_markup=markup,
    )

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    if text == 'застряла игрушка':
        return TOYS
    else:
        return GET_TABLE_EROR