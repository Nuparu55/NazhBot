from pymongo import collection
import config
import telebot
import logging
import data
import notesDB


#логирование
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

#создаем экземпляр бота
bot = telebot.TeleBot(config.TOKEN)


#создаем клавиатуру
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
addItem = telebot.types.KeyboardButton(data.Answer.Add)
delItem = telebot.types.KeyboardButton(data.Answer.Delete)
showItems = telebot.types.KeyboardButton(data.Answer.Show)
clearItems = telebot.types.KeyboardButton(data.Answer.Clear)
markup.add(addItem)
markup.add(delItem)
markup.add(showItems)
markup.add(clearItems)

#чистая клавиатура
emptyMarkup = telebot.types.ReplyKeyboardRemove(selective=False)

#старт
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я бот с деревенскими заметками", reply_markup=markup)

#обработчик сообщений
@bot.message_handler(content_types='text')
def msg_reply(msg):
    match msg.text:
        case data.Answer.Add:
            answer = bot.send_message(msg.chat.id, f'Что добавляем?', reply_markup=emptyMarkup)
            bot.register_next_step_handler(answer, add_item)
        case data.Answer.Delete:
            notes = notesDB.GetNotes()
            if (notes.count() == 0):
                bot.send_message(msg.chat.id, f'Нет заметок', reply_markup=markup)
            else:
                listMarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                for item in notes:
                    listMarkup.add(telebot.types.KeyboardButton(item['note']))
                answer = bot.send_message(msg.chat.id, f'Что удаляем?', reply_markup=listMarkup)
                bot.register_next_step_handler(answer, del_item)
        case data.Answer.Show:
            notes = notesDB.GetNotes()
            if (notes.count() == 0):
                bot.send_message(msg.chat.id, f'Нет заметок', reply_markup=markup)
            else:
                listed = ""
                for n in notes:
                    listed += n['note'] + '\n'
                bot.send_message(msg.chat.id, f'Список заметок:\n{listed}', reply_markup=markup)
        case data.Answer.Clear:
            notesDB.ClearNotes()
            bot.send_message(msg.chat.id, f'Заметки очищены', reply_markup=markup)
        case _:
            bot.send_message(msg.chat.id, f'Неизвестная команда', reply_markup=markup)

def add_item(msg):
    isAlreadyExist = notesDB.NoteExist(msg.text)

    if isAlreadyExist:
        bot.send_message(msg.chat.id, f'{msg.text} уже есть в списке', reply_markup=markup)
    else:
        notesDB.InsertNote(msg.text)
        bot.send_message(msg.chat.id, f'Добавил {msg.text} в список', reply_markup=markup)

def del_item(msg):
    notesDB.DelNote(msg.text)

    bot.send_message(msg.chat.id, f'Удалил {msg.text} из списка', reply_markup=markup)

bot.infinity_polling()