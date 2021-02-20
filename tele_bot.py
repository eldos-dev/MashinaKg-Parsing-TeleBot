from my_bot_token import TOKEN
from telebot import types
from parser import main
import telebot
import json

token = TOKEN

bot = telebot.TeleBot(token)

# open and read json file
def get_dict():
    json_file = open('mashina_kg.json')
    data = json.load(json_file)
    json_file.close()
    list_dict = [dict(elem) for elem in data]
    return list_dict

# Create buttons category
reply_keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
k1 = types.KeyboardButton('Легковые авто')
k2 = types.KeyboardButton('Коммерческие авто')
k3 = types.KeyboardButton('Спецтехника')
k4 = types.KeyboardButton('Мотоциклы')
reply_keyboards.add(k1, k2, k3, k4)

# Start message
@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Выберите категорию:', reply_markup=reply_keyboards)
    bot.register_next_step_handler(msg, get_func)

# Choice category
def get_func(message):
    if message.text == 'Легковые авто':
        url = 'search/all/'
        main(url)
    if message.text == 'Коммерческие авто':
        main('commercialsearch/all/')
    if message.text == 'Спецтехника':
        main('specsearch/all/')
    if message.text == 'Мотоциклы':
        main('motosearch/all/')
    get_start(message)

# Create buttons
def get_inline_keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    list_dict = get_dict()
    count = 1
    for dict_ in list_dict:
        batton = types.InlineKeyboardButton(f"{count} - {dict_.get('title')}", callback_data=f'{count}')
        count += 1
        inline_keyboard.add(batton)
    return inline_keyboard


def get_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Приветсвую, {message.chat.first_name}. Выберите машину', reply_markup=get_inline_keyboard())

# Create buttons 'back' & 'exit'
keyboards = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Назад', callback_data='back to list')
btn2 = types.InlineKeyboardButton('Вернуться в категорию', callback_data='back to category')
btn3 = types.InlineKeyboardButton('Выйти', callback_data='exit')
keyboards.add(btn1, btn2, btn3)

@bot.callback_query_handler(func=lambda c: True)
def show_discription(c):
    chat_id = c.message.chat.id
    if c.data == 'back to list':
        bot.edit_message_text('Вы вернулись в список', chat_id, c.message.message_id, reply_markup=get_inline_keyboard())
    # elif c.data == 'back to category':
    #     bot.edit_message_text('Вы вернулись в категорию', chat_id, c.message.message_id, reply_markup=start_message)
    elif c.data == 'exit':
        bot.edit_message_text(f'Досвидания, наш дорогой пользователь!', chat_id, c.message.message_id, reply_markup=None)
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK5TmAJEsAJxfQhYwOJFvrcYJqeVJJPAAJhAANOXNIpSmNxpUypVW4eBA')
    else:
        list_dict = get_dict()
        dict_ = list(list_dict[int(c.data) - 1].values())
        dict_2 = list(dict_[2].values())
        bot.edit_message_text(f'Модель:  {dict_[0]}\n фото:  {dict_[1]} \n Цена:  {dict_2[0]} \nГод:  {dict_2[1]} \nДвигатель:  {dict_2[2]} \nРуль:  {dict_2[3]}',
                        chat_id,
                        c.message.message_id,
                        reply_markup=keyboards)

bot.polling()