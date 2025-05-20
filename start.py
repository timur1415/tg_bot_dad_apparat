from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)

from states import MAIN_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("клешня не закрывается", callback_data="dont_clos")],
        [InlineKeyboardButton("кнопка залипла", callback_data="tap")],
        [InlineKeyboardButton("джойстик не работает", callback_data="dont_work")],
        [
            InlineKeyboardButton(
                "после оплаты картой игра не началась", callback_data="banc card"
            )
        ],
        [
            InlineKeyboardButton(
                "после оплаты монетой игра не началась", callback_data="coin"
            )
        ],
        [
            InlineKeyboardButton(
                "после оплаты купюрой игра не началась", callback_data="money"
            )
        ],
        [InlineKeyboardButton("застряла игрушка", callback_data="toys")],
        [InlineKeyboardButton("клешня не открывается", callback_data="dont_close")],
        [InlineKeyboardButton("нет в этом списке", callback_data="no_in_sp")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if query:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"добро пожаловать {update.effective_user.first_name},что случилось?",
            reply_markup=markup,
        )

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"добро пожаловать {update.effective_user.first_name},что случилось?",
            reply_markup=markup,
        )
        return MAIN_MENU