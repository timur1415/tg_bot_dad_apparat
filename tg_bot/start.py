from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ContextTypes,
)

from config.states import MAIN_MENU, OPROS_MENU

from config.config import ADMIN_ID, WEBHOOK_URL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Опрос", callback_data="opros")]]

    user_id = update.effective_user.id if update.effective_user else None
    if ADMIN_ID and user_id == ADMIN_ID:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "Админ панель", web_app=WebAppInfo(url=f"{WEBHOOK_URL}/app")
                )
            ]
        )

    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Привет! Я помогу быстро оформить заявку по автомату.\n"
            "Выберите действие ниже."
        ),
        reply_markup=markup,
    )
    return MAIN_MENU


async def start_opros(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            text=(
                f"{update.effective_user.first_name}, выберите проблему из списка ниже."
            ),
            reply_markup=markup,
        )

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"{update.effective_user.first_name}, выберите проблему из списка ниже."
            ),
            reply_markup=markup,
        )
    return OPROS_MENU
