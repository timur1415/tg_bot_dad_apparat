keyboard = [['клешня не закрывается'], ['кнопка залипла'], ['джойстик не работает'], ['после оплаты картой игра не началась'], ['после оплаты монетой игра не началась'], ['после оплаты купюрой игра не началась'], ['застряла игрушка'], ['клешня не открывается'],['нет в этом списке']]

#     elif update.effective_message.text == "нет в этом списке":
#         await context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Пожалуйста, сформулируйте проблему, чтобы мы могли внести её в бота.",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#         return NO_IN_SP


# async def no_in_sp(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["trable"] = update.effective_message.text
#     print(context.user_data["trable"])
#     keyboard = [["01", "02", "03", "04", "нет"]]
#     markup = ReplyKeyboardMarkup(keyboard)
#     await context.bot.send_photo(
#         chat_id=update.effective_chat.id,
#         photo=open("photo/table.jpg", "rb"),
#         caption="Посмотрите, пожалуйста, есть ли на табло (которое показано на фото, там где ноль) ошибка, которая дана на клавиатуре.",
#         reply_markup=markup,
#     )
#     return GET_ERROR 