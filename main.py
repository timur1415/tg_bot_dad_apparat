import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    PicklePersistence,
    CallbackQueryHandler,
)
from start import start, security
from opros import (
    get_table_eror,
    get_address,
    get_error,
    get_money,
    tanks,
    no_in_sp,
    toys,
    banknote,
    banknote_handler
)
import asyncio

from states import (
    GET_TABLE_EROR,
    GET_ADDRESS,
    GET_ERROR,
    GET_MONEY,
    TANKS,
    NO_IN_SP,
    TOYS,
    SECURITY,
    BANKNOTE,
    RESTART
)



import os
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    perrsistece = PicklePersistence(filepath="apparat_bot")
    application = (
        ApplicationBuilder().token(os.getenv("TOKEN")).persistence(perrsistece).build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SECURITY:[MessageHandler(filters.TEXT & ~filters.COMMAND, security)],
            GET_TABLE_EROR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_table_eror)
            ],
            GET_ERROR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_error)],
            GET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            GET_MONEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_money)],
            NO_IN_SP: [MessageHandler(filters.TEXT & ~filters.COMMAND, no_in_sp)],
            TOYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, toys),
                   CallbackQueryHandler(start, pattern='^back$')],
            TANKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, tanks),
                    CallbackQueryHandler(start, pattern='^exit$')],
            BANKNOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, banknote_handler)]
        },
        fallbacks=[CommandHandler("start", start)],
        name="apparat_bot",
        persistent=True,
    )

    application.add_handler(conv_handler)

    application.run_polling()
