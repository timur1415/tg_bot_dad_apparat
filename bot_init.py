from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config.config import TOKEN
from tg_bot.opros import (
    banknote,
    get_address,
    get_money,
    get_phone_contact,
    get_phone_text_fallback,
    get_refund_method,
    get_rek,
    get_table_eror,
    no_in_sp,
    tanks,
    toys,
)
from tg_bot.start import start
from config.states import (
    BANKNOTE,
    GET_ADDRESS,
    GET_CRED,
    GET_MONEY,
    GET_REK,
    GET_TABLE_EROR,
    MAIN_MENU,
    NO_IN_SP,
    TANKS,
    TOYS,
)


def build_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(toys, pattern="^toys$"),
                CallbackQueryHandler(get_address, pattern="^dont_clos$"),
                CallbackQueryHandler(get_address, pattern="^tap$"),
                CallbackQueryHandler(get_table_eror, pattern="^dont_work$"),
                CallbackQueryHandler(get_table_eror, pattern="^banc card$"),
                CallbackQueryHandler(get_table_eror, pattern="^coin$"),
                CallbackQueryHandler(banknote, pattern="^money$"),
                CallbackQueryHandler(get_table_eror, pattern="^dont_close$"),
                CallbackQueryHandler(no_in_sp, pattern="no_in_sp"),
            ],
            GET_TABLE_EROR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_table_eror)
            ],
            GET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            GET_MONEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_money)],
            NO_IN_SP: [MessageHandler(filters.TEXT & ~filters.COMMAND, no_in_sp)],
            TOYS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, toys),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            TANKS: [
                MessageHandler(filters.CONTACT, get_phone_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_text_fallback),
                CallbackQueryHandler(start, pattern="^exit$"),
            ],
            GET_CRED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_refund_method)
            ],
            BANKNOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, tanks)],
            GET_REK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rek)],
        },
        fallbacks=[CommandHandler("start", start)],
        name="apparat_bot",
        persistent=False,
    )


def create_application() -> Application:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(build_conversation_handler())
    return application


def create_aplication() -> Application:
    # Backward compatible alias for old misspelled name.
    return create_application()
