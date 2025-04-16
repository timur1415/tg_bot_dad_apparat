from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
)
from states import GET_ERROR, GET_ADDRESS, GET_MONEY, NO_IN_SP, TANKS

import os
from dotenv import load_dotenv
load_dotenv()

async def get_table_eror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text != "нет в этом списке":
        context.user_data["trable"] = update.effective_message.text
        print(context.user_data["trable"])
        keyboard = [["01", "02", "03", "04", "нет"]]
        markup = ReplyKeyboardMarkup(keyboard)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("photo/table.jpg", "rb"),
            caption="Посмотрите, пожалуйста, есть ли на табло (которое показано на фото, там где ноль) ошибка, которая дана на клавиатуре.",
            reply_markup=markup,
        )
        return GET_ERROR
    
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пожалуйста, сформулируйте проблему, чтобы мы могли внести её в бота.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NO_IN_SP


async def no_in_sp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trable"] = update.effective_message.text
    print(context.user_data["trable"])
    keyboard = [["01", "02", "03", "04", "нет"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/table.jpg", "rb"),
        caption="Посмотрите, пожалуйста, есть ли на табло (которое показано на фото, там где ноль) ошибка, которая дана на клавиатуре.",
        reply_markup=markup,
    )
    return GET_ERROR


async def get_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text != "нету":
        context.user_data["table_eror"] = update.effective_message.text
        print(context.user_data["table_eror"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Попробуйте отключить аппарат от розетки и снова включить. Если это не поможет, полностью отключите питание и сообщите адрес и номер автомата.\n\nгород/улица номер.",
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
        text="Для возврата денег необходимо предоставить реквизиты ❗️В ОДНОМ СООБЩЕНИИ❗️\n\n1. Номер телефона, имя получателя и банк\n\n2. Номер карты\n\nДоступно два варианта оформления",
    )
    return TANKS


async def tanks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rek"] = update.effective_message.text
    print(context.user_data["rek"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Благодарим за обращение! Заявка будет оформлена в течение недели. Мы устраним неисправность и вернём вам средства.\n\nИспользуйте /start для нового обращения",
    )
    keyboard = [
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
    await context.bot.send_message(
        chat_id=int(os.getenv('ADMIN_ID')),
        text=f"{context.user_data['trable']} - это проблема которая случилась с ботом\n\n{context.user_data['table_eror']} - ошибка на табло\n\n{context.user_data['address']} - адрес аппарата\n\n{context.user_data['money']} - сколько человек потратил\n\n{context.user_data['rek']} - реквизиты человека",
    )

    if context.user_data["trable"] not in keyboard:
        await context.bot.send_message(
            chat_id=int(os.getenv('MY_ID')),
            text=f"добавить проблему в бота:\n\n{context.user_data['trable']}",
        )