from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,

    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from states import GET_ERROR, GET_ADDRESS, GET_MONEY, GET_TABLE_EROR, TANKS, TOYS, BANKNOTE

import os
from dotenv import load_dotenv

load_dotenv()

async def banknote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔴', '🟢']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Какой сейчас цвет индикатора на купюрнике: красный или зеленый?",
        reply_markup=markup,
    )

    return BANKNOTE

async def banknote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['color'] == update.effective_message.text
    if context.user_data['color'] == '🔴':

        return GET_ADDRESS
    
    else:
        pass

async def toys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("описать проблему заново", callback_data="back")]]
    markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    user_name = update.effective_user.name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="В ближайшее время с вами свяжется наш специалист. Вы сможете отправить ему фото застрявшей игрушки, и он подскажет, как решить проблему. Если ничего не получится — гарантируем возврат денег.\n\nДавайте разберёмся вместе! 😊",
        reply_markup=markup,
    )

    # await context.bot.send_message(
    #         chat_id=int(os.getenv('MY_ID')),
    #         text=f'{user_name} - у этого типа игрушка застряла нужно помочь')

    return TOYS


async def get_table_eror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trable"] = update.effective_message.text
    print(context.user_data["trable"])
    query = update.callback_query
    if query:
        keyboard = [["01", "02", "03", "04", "нет"]]
        markup = ReplyKeyboardMarkup(keyboard)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("photo/table.jpg", "rb"),
            caption="Посмотрите, пожалуйста, что гарит на табло и выберете на клавиатуре",
            reply_markup=markup,
        )
    else:
        keyboard = [["00", "01", "02", "03", "04"]]
        markup = ReplyKeyboardMarkup(keyboard)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("photo/table.jpg", "rb"),
            caption="Посмотрите, пожалуйста, что гарит на табло и выберете на клавиатуре",
            reply_markup=markup,
        )
    return GET_ERROR


async def no_in_sp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, сформулируйте проблему, чтобы мы могли внести её в бота.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GET_TABLE_EROR


async def get_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text != "нету":
        context.user_data["table_eror"] = update.effective_message.text
        print(context.user_data["table_eror"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Попробуйте отключить аппарат от розетки и снова включить. Если это не поможет, ❗️ПОЛНОСЬТЮ ОТКЛЮЧИТЕ ПИТАНИЕ❗️ и сообщите адрес и номер автомата.\n\nгород/улица номер.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GET_ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.effective_message.text
    print(context.user_data["address"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="сколько вы потратили?"
    )
    return GET_MONEY


async def get_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["money"] = update.effective_message.text
    print(context.user_data["money"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Для возврата денег необходимо предоставить реквизиты ❗️В ОДНОМ СООБЩЕНИИ❗️\n\n1. Номер телефона, имя получателя и банк\n\n2. Номер карты, имя получателя\n\nДоступно два варианта оформления",
    )
    return TANKS


async def tanks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("описать проблему заново", callback_data="exit")]]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data["rek"] = update.effective_message.text
    print(context.user_data["rek"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Благодарим за обращение! Заявка будет оформлена в течение недели. Мы устраним неисправность и вернём вам средства.",
        reply_markup=markup,
    )
    sp = [
        "клешня не закрывается",
        "кнопка залипла",
        "джойстик не работает",
        "после оплаты картой игра не началась",
        "после оплаты монетой игра не началась",
        "после оплаты купюрой игра не началась",
        "застряла игрушка",
        "клешня не открывается",
        "нет в этом списке",
    ]
    # await context.bot.send_message(
    #     chat_id=int(os.getenv('MY_ID')),
    #     text=f"{context.user_data['trable']} - это проблема которая случилась с ботом\n\n{context.user_data['table_eror']} - ошибка на табло\n\n{context.user_data['address']} - адрес аппарата\n\n{context.user_data['money']} - сколько человек потратил\n\n{context.user_data['rek']} - реквизиты человека",
    # )
    # if context.user_data["trable"] not in sp:
    #     await context.bot.send_message(
    #         chat_id=int(os.getenv('MY_ID')),
    #         text=f"добавить проблему в бота:\n\n{context.user_data['trable']}",
    #     )
