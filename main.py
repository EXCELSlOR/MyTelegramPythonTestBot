import telebot

bot = telebot.TeleBot('8181700980:AAFw-EsOg3F0CUdkyVETdLS5LqKMQbTOvew')


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет!")


bot.infinity_polling()
