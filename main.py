import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from start import start
from opros import get_table_eror, get_address, get_error, get_money, tanks, no_in_sp
from states import GET_TABLE_EROR, GET_ADDRESS, GET_ERROR, GET_MONEY, TANKS, NO_IN_SP
import os 
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(os.getenv("TOKEN"))
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_TABLE_EROR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_table_eror)
            ],
            GET_ERROR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_error)
            ],
            GET_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)
            ],
            GET_MONEY: [MessageHandler(filters.TEXT & ~filters.COMMAND,get_money)
            ],
            NO_IN_SP: [MessageHandler(filters.TEXT & ~filters.COMMAND,no_in_sp)
            ],
            TANKS: [MessageHandler(filters.TEXT & ~filters.COMMAND,tanks)
            ]

        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()