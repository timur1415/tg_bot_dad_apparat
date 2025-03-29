import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from start import start
from opros import get_table_eror, get_adres
(
GET_TABLE_EROR,
GET_ADRES,# спрашиваю адрес
GET_MONEY,#спрашиваю сколько потратил 
) = range(3)



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



if __name__ == '__main__':
    application = ApplicationBuilder().token('7750373892:AAF3YiYv8omzRPMqD0dHumyLtWxIf8pqW10').build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
         states={
            GET_TABLE_EROR:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_table_eror)],
            GET_ADRES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_adres)]
                 
        
        },
        fallbacks=[CommandHandler('start', start)])
    
    

    application.add_handler(conv_handler)
    
    application.run_polling()