from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    GET_ADDRESS,
    GET_MONEY,
    GET_CRED,
    TANKS,
    TOYS,
    TOYS_MACHINE_INFO,
    BANKNOTE,
    GET_REK,
)

import os
from dotenv import load_dotenv
from tg_bot.problems import dic_problems
from db.users_crud import save_request

load_dotenv()


def _admin_chat_id() -> int | None:
    raw_id = os.getenv("ADMIN_ID") or os.getenv("MY_ID")
    if not raw_id:
        return None
    try:
        return int(raw_id)
    except ValueError:
        return None


def _build_admin_text(context_data: dict, request_id: int, created_at: str, user) -> str:
    problem = context_data.get("trable", "Не указано")
    table_error = context_data.get("table_eror") or "Не указано"
    machine_info = context_data.get("address", "Не указано")
    amount = context_data.get("money") or "Не указано"
    phone = context_data.get("phone") or "Не указано"
    refund_method = context_data.get("refund_method") or "Не указано"
    requisites = context_data.get("rek") or "Не указано"

    return (
        f"Новая заявка #{request_id}\n"
        f"Дата: {created_at}\n"
        f"Пользователь: {user.full_name} (@{user.username or 'без username'})\n"
        f"ID пользователя: {user.id}\n\n"
        f"Проблема: {problem}\n"
        f"Ошибка на табло: {table_error}\n"
        f"Информация об автомате: {machine_info}\n"
        f"Сумма: {amount}\n"
        f"Телефон: {phone}\n"
        f"Способ возврата: {refund_method}\n"
        f"Реквизиты: {requisites}"
    )


def _normalize_phone(text: str) -> str | None:
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) == 11 and digits[0] in {"7", "8"}:
        return "+7" + digits[1:]
    if len(digits) == 10:
        return "+7" + digits
    return None


async def banknote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["trable"] = dic_problems[query.data]
    keyboard = [["🔴", "🟢"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Какой сейчас цвет индикатора на купюрнике: красный или зеленый?",
        reply_markup=markup,
    )

    return GET_ADDRESS


async def toys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        context.user_data["trable"] = dic_problems[query.data]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отправьте, пожалуйста, фото застрявшей игрушки.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return TOYS

    message = update.effective_message
    if not message or not message.photo:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Нужна именно фотография. Пришлите фото застрявшей игрушки.",
        )
        return TOYS

    photo_file_id = message.photo[-1].file_id
    context.user_data["toys_photo_file_id"] = photo_file_id

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Теперь отправьте отдельным сообщением адрес и номер автомата.",
    )
    return TOYS_MACHINE_INFO


async def toys_machine_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    machine_info = (update.effective_message.text or "").strip() or "Не указано"
    photo_file_id = context.user_data.get("toys_photo_file_id")

    if not photo_file_id:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Сначала пришлите фото застрявшей игрушки.",
        )
        return TOYS

    user = update.effective_user
    request_id, created_at = save_request(
        user_id=user.id if user else None,
        username=user.username if user else None,
        full_name=user.full_name if user else None,
        machine_info=machine_info,
        problem=context.user_data.get("trable", "Застряла игрушка"),
        table_error=None,
        amount=None,
        requisites="Фото застрявшей игрушки",
        photo_file_id=photo_file_id,
    )

    keyboard = [[InlineKeyboardButton("Описать еще одну проблему", callback_data="back")]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Спасибо, фото получили. Заявка создана и передана специалисту.\n\n"
            "Если нужно, можете сразу описать еще одну проблему."
        ),
        reply_markup=markup,
    )

    admin_id = _admin_chat_id()
    if admin_id and user:
        text = _build_admin_text(context.user_data, request_id, created_at, user)
        await context.bot.send_message(chat_id=admin_id, text=text)
        await context.bot.send_photo(chat_id=admin_id, photo=photo_file_id)

    context.user_data.clear()
    return TOYS


async def toys_text_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, отправьте фото застрявшей игрушки, чтобы создать заявку.",
    )
    return TOYS


async def toys_machine_info_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Отправьте, пожалуйста, текстом адрес и номер автомата.",
    )
    return TOYS_MACHINE_INFO


async def get_table_eror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return GET_ADDRESS
    await query.answer()
    context.user_data["trable"] = dic_problems[query.data]
    keyboard = [["01", "02", "03", "04"], ["нет"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/table.jpg", "rb"),
        caption="Посмотрите, пожалуйста, что горит на табло и выберете на клавиатуре",
        reply_markup=markup,
    )
    return GET_ADDRESS


async def no_in_sp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, сформулируйте проблему, чтобы мы могли внести её в бота.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GET_ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query:
        await query.answer()
        context.user_data["trable"] = dic_problems[query.data]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Попробуйте отключить аппарат от розетки и снова включить. Если это не поможет, ❗️ПОЛНОСТЬЮ ОТКЛЮЧИТЕ ПИТАНИЕ❗️ и сообщите адрес и номер автомата.\n\nгород/улица номер.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        message_text = (update.effective_message.text or "").strip()
        known_table_values = {"01", "02", "03", "04", "нет", "🔴", "🟢"}

        if message_text in known_table_values:
            context.user_data["table_eror"] = message_text
        elif context.user_data.get("trable"):
            # Problem is already chosen in callback flow; treat free text here as indicator/table value.
            context.user_data["table_eror"] = message_text
        else:
            # no_in_sp flow: user enters custom problem text.
            context.user_data["trable"] = message_text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Попробуйте отключить аппарат от розетки и снова включить. Если это не поможет, ❗️ПОЛНОСТЬЮ ОТКЛЮЧИТЕ ПИТАНИЕ❗️ и сообщите адрес и номер автомата.\n\nгород/улица номер.",
            reply_markup=ReplyKeyboardRemove(),
        )
    return GET_MONEY


async def get_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Сколько вы потратили?"
    )
    return GET_REK


async def get_rek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["money"] = update.effective_message.text
    keyboard = [[KeyboardButton("Поделиться номером", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Оставьте номер телефона для связи.\n"
            "Нажмите кнопку ниже, чтобы отправить номер через Telegram."
        ),
        reply_markup=markup,
    )
    return TANKS


async def get_phone_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.effective_message.contact
    user = update.effective_user

    if not contact or not user or contact.user_id != user.id:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отправьте именно свой контакт через кнопку 'Поделиться номером'.",
        )
        return TANKS

    phone = _normalize_phone(contact.phone_number)
    if not phone:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Не удалось прочитать номер из контакта. Нажмите кнопку и отправьте контакт еще раз.",
        )
        return TANKS

    context.user_data["phone"] = phone
    keyboard = [["По номеру телефона"], ["По номеру карты"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите способ возврата:",
        reply_markup=markup,
    )
    return GET_CRED


async def get_phone_text_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Поделиться номером", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Номер нужно отправить через кнопку 'Поделиться номером', обычный текст не подходит.",
        reply_markup=markup,
    )
    return TANKS


async def get_refund_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    method = update.effective_message.text.strip()
    allowed_methods = {"По номеру телефона", "По номеру карты"}

    if method not in allowed_methods:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите способ из кнопок: По номеру телефона или По номеру карты.",
        )
        return GET_CRED

    context.user_data["refund_method"] = method
    prompt_text = (
        "Отправьте одним сообщением:  имя получателя и банк."
        if method == "По номеру телефона"
        else "Отправьте одним сообщением: номер карты и имя получателя."
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=prompt_text,
        reply_markup=ReplyKeyboardRemove(),
    )
    return BANKNOTE


async def tanks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Описать ещё одну проблему", callback_data="exit")]]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data["rek"] = update.effective_message.text

    user = update.effective_user
    request_id, created_at = save_request(
        user_id=user.id if user else None,
        username=user.username if user else None,
        full_name=user.full_name if user else None,
        machine_info=context.user_data.get("address", ""),
        problem=context.user_data.get("trable", "Не указано"),
        table_error=context.user_data.get("table_eror"),
        amount=context.user_data.get("money"),
        requisites=(
            f"Телефон: {context.user_data.get('phone', 'Не указано')}\n"
            f"Способ возврата: {context.user_data.get('refund_method', 'Не указано')}\n"
            f"Данные для возврата: {context.user_data.get('rek', 'Не указано')}"
        ),
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Спасибо за заявку. Скоро всё вернем.\n\n"
            "❗️ ПРОСИМ ВАС: отсоедините автомат от розетки."
        ),
        reply_markup=markup,
    )

    admin_id = _admin_chat_id()
    if admin_id and user:
        text = _build_admin_text(context.user_data, request_id, created_at, user)
        await context.bot.send_message(chat_id=admin_id, text=text)

        if context.user_data.get("trable") not in dic_problems.values():
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"Добавить проблему в бота:\n\n{context.user_data.get('trable')}",
            )

    context.user_data.clear()
