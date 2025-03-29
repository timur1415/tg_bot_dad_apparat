import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from states import GET_ERROR, GET_ADDRESS, GET_MONEY, NO_IN_SP, TANKS


async def get_table_eror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trable"] = update.effective_message.text
    print(context.user_data["trable"])
    keyboard = [["01", "02", "03", "04", "нету"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/table.jpg", "rb"),
        caption="посмотрите пожалуйста есть ли на табло которое показано на фото(там где нолик) ошибка которая днна на клавиотуре",
        reply_markup=markup
    )
    return GET_ERROR


async def get_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text != "нету":
        context.user_data["table_eror"] = update.effective_message.text
        print(context.user_data["table_eror"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="попробуйте выключить из разетки и включить обратно, если не помогло то выключите из разетки и напиши адрес и номер автомата\n\nгород/улица номер",reply_markup=ReplyKeyboardRemove()
    )
    return GET_ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.effective_message.text
    print(context.user_data["address"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="сколько потратил"
    )
    return GET_MONEY


async def get_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["money"] = update.effective_message.text
    print(context.user_data["money"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="для того что мы могли вернуть вам деньги вы должны скинуть нам свои реквизиты\n\n1. номер телефона/имя получателя/банк\n\n2. номер карты\n\nна выбор два варианта",
    )
    return NO_IN_SP

async def no_in_sp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["props"] = update.effective_message.text
    if context.user_data["trable"] == 'нет в этом списке':
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="поскольку вы выброли что в списке бота нет такой проблемы которая случилась с нашим аппаратом.\n\nопишите проблему\n\nобразец - первое сообщение"
    )
        return TANKS
    elif context.user_data["trable"] != 'нет в этом списке':
        return TANKS
    

async def tanks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trable_no_in_in_sp"] = update.effective_message.text
    print(context.user_data["trable_no_in_in_sp"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="спасибо за ваше время мы составим заявку в течение недели всё починим и вернём вам деньги!!!\n\n/start что бы начать заново",
    )
