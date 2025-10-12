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
    context.user_data.clear()
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Клешня не закрывается", callback_data="dont_clos")],
        [InlineKeyboardButton("Кнопка залипла", callback_data="tap")],
        [InlineKeyboardButton("Джойстик не работает", callback_data="dont_work")],
        [
            InlineKeyboardButton(
                "После оплаты картой игра не началась", callback_data="banc card"
            )
        ],
        [
            InlineKeyboardButton(
                "После оплаты монетой игра не началась", callback_data="coin"
            )
        ],
        [
            InlineKeyboardButton(
                "После оплаты купюрой игра не началась", callback_data="money"
            )
        ],
        [InlineKeyboardButton("Застряла игрушка", callback_data="toys")],
        [InlineKeyboardButton("Клешня не открывается", callback_data="dont_close")],
        [InlineKeyboardButton("Нет в этом списке", callback_data="no_in_sp")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(
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