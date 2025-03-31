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
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text='Я тоже!'))
    keyboard.add(telebot.types.KeyboardButton(text='Мы уже знакомы...'))
    bot.send_message(chat_id, f"Рад знакомству, {name}", reply_markup=keyboard)
    bot.register_next_step_handler(message, send_reply_message)


def send_reply_message(message):
    chat_id = message.chat.id
    message_text = message.text
    if message_text == 'Я тоже!':
        bot.send_message(chat_id, 'Приятно слышать')
    else:
        bot.send_message(chat_id, 'Прости, не узнал тебя. Богатым будешь!')


bot.infinity_polling()