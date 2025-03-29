import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
(
MAIN_MENU,
GET_TABLE_EROR,
GET_ADRES,# спрашиваю адрес
GET_MONEY,#спрашиваю сколько потратил 
) = range(4)


async def get_table_eror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trable"] = update.effective_message.text
    print(context.user_data["trable"])
    keyboard = [["01", "02", "03", "04", 'нету']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/table.jpng", "rb"),
        caption="посмотрите пожалуйста есть ли на табло которое показано на фото(там где нолик) ошибка которая днна на клавиотуре",
        reply_markup=markup
    )
    if update.effective_message.text == 'нету':
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="попробуйте выключить из разетки и включить обратно, если не помогло то выключите из разетки",
    )
        return GET_ADRES


async def get_adres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["table_eror"] = update.effective_message.text
    print(context.user_data["table_eror"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="попробуйте выключить из разетки и включить обратно, если не помогло то выключите из разетки и напиши адрес и номер автомата\n\nгород/улица номер",
    )
