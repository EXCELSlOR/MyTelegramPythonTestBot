import telebot

bot = telebot.TeleBot('8181700980:AAFw-EsOg3F0CUdkyVETdLS5LqKMQbTOvew')


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Как тебя зовут?")
    bot.register_next_step_handler(message, get_user_name)


def get_user_name(message):
    chat_id = message.chat.id
    name = message.text
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Я тоже!', callback_data='me_too'),
        telebot.types.InlineKeyboardButton(
            text='Мы уже знакомы...', callback_data='already_known'))
    bot.send_message(chat_id, f"Рад знакомству, {name}", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'me_too')
def me_too(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Приятно слышать!')


@bot.callback_query_handler(func=lambda call: call.data == 'already_known')
def already_known(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Прости, не узнал тебя. Богатым будешь!')


bot.infinity_polling()