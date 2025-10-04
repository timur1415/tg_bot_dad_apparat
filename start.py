from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)



from opros import toys, get_address, get_table_eror, banknote, no_in_sp


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        ["застряла игрушка"],
        ["клешня не открывается"],
        ["кнопка залипла"],
        ["Джойстик не работает"],
        ["После оплаты картой игра не началась"],
        ["После оплаты монетой игра не началась"],
        ["После оплаты купюрой игра не началась"],
        ["Клешня не закрывается"],
        ["нет в этом списке"],
    ]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
        text=f"добро пожаловать {update.effective_user.first_name},что случилось?",
        reply_markup=markup,
    )

async def security(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['main_trable'] = update.effective_message.text
    if context.user_data['main_trable'] == 'застряла игрушка':
        return toys
    elif context.user_data['main_trable'] == 'Клешня не открывается':
        return get_address
    elif context.user_data['main_trable'] == 'Кнопка залипла':
        return get_address
    elif context.user_data['main_trable'] == 'Джойстик не работает':
        return get_table_eror
    elif context.user_data['main_trable'] == 'После оплаты картой игра не началась':
        return get_table_eror
    elif context.user_data['main_trable'] == 'После оплаты монетой игра не началась':
        return get_table_eror
    elif context.user_data['main_trable'] == 'После оплаты купюрой игра не началась':
        return banknote
    elif context.user_data['main_trable'] == 'Клешня не закрывается':
        return get_table_eror
    elif context.user_data['main_trable']  == 'нет в этом списке':
        return no_in_sp
    else:
        return dif
    
async def dif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Иди нах клоун",
    )