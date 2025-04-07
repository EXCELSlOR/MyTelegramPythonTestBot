import telebot
import parser
from parser import QuizParser

parser = QuizParser()
bot = telebot.TeleBot('8181700980:AAHIj3zK-LzWr-9F5TS1z6xCFL4HM3VrhT0')


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text='Начать'))
    bot.send_message(chat_id, 'Для начала викторины нажмите кнопку "Начать"', reply_markup=keyboard)
    bot.register_next_step_handler(message, show_question)


def show_question(message):
    chat_id = message.chat.id
    result = parser.get_new_question()
    question_id = result['question_id']
    question = result['question_text']
    answers = result['answers']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(answers)):
        keyboard.add(telebot.types.KeyboardButton(text=answers[i]))
    bot.send_message(chat_id, f"Вопрос №{question_id}: {question}", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_answer)


def get_answer(message):
    chat_id = message.chat.id
    result = parser.check_answer(message.text)
    correct_answer = result['correct_answer']
    statistics = result['statistics']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text='Следующий вопрос'))
    message_text = "Верно" if result['correct'] else "Неверно"
    bot.send_message(chat_id, f"{message_text}! Правильный ответ: {correct_answer}\n{statistics}",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, show_question)


bot.infinity_polling()
