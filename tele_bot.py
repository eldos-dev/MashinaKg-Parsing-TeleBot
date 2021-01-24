from my_bot_token import TOKEN
from telebot import types
from parsing import main
import telebot
import json

token = TOKEN

bot = telebot.TeleBot(token)

def get_dict():
    json_file = open('mashina_kg.json')
    data = json.load(json_file)
    json_file.close()
    list_dict = [dict(elem) for elem in data]
    return list_dict

# Create buttons
inline_keyboard = types.InlineKeyboardMarkup()

@bot.message_handler(commands=['start', 'hello'])
def start(message):
    main()
    chat_id = message.chat.id

    list_dict = get_dict()
    count = 1
    for dict_ in list_dict:
        batton = types.InlineKeyboardButton(f"{count} - {dict_.get('title')}", callback_data=f'{count}')
        count += 1
        inline_keyboard.add(batton)
    bot.send_message(chat_id, f'Приветсвую, {message.chat.first_name}. Выберите машину', reply_markup=inline_keyboard)

# Create buttons 'back' & 'exit'
keyboards = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Назад', callback_data='back')
btn2 = types.InlineKeyboardButton('Выйти', callback_data='exit')
keyboards.add(btn1, btn2)

@bot.callback_query_handler(func=lambda c: True)
def show_discription(c):
    chat_id = c.message.chat.id
    if c.data == 'back':
        bot.send_message(chat_id, 'Вы вернулись в список', reply_markup=inline_keyboard)
    elif c.data == 'exit':
        bot.send_message(chat_id, 'Досвидания', reply_markup=None)
    else:
        list_dict = get_dict()
        dict_ = list(list_dict[int(c.data) - 1].values())
        dict_2 = list(dict_[2].values())
        bot.send_message(chat_id,
                        f'Модель:  {dict_[0]}\n фото:  {dict_[1]} \n Цена:  {dict_2[0]} \nГод:  {dict_2[1]} \nДвигатель:  {dict_2[2]} \nРуль:  {dict_2[3]}',
                        reply_markup=keyboards)

bot.polling()