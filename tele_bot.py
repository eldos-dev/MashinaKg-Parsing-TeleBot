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

inline_keyboard = types.InlineKeyboardMarkup()
keyboards = types.InlineKeyboardMarkup()

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


@bot.callback_query_handler(func=lambda c: True)
def show_discription(c):
    btn1 = types.InlineKeyboardButton('Выйти')
    btn2 = types.InlineKeyboardButton('Назад')
    keyboards.add(btn1, btn2)
    chat_id = c.message.chat.id
    list_dict = get_dict()
    dict_ = list(list_dict[int(c.data) - 1].values())
    dict_2 = list(dict_[2].values())
    list_ = dict_2[3].split(',')
    bot.send_message(chat_id, 
                    f'Модель:  {dict_[0]}\n фото:  {dict_[1]} \n Цена:  {dict_2[0]} \nГод:  {dict_2[1]} \nДвигатель:  {dict_2[2]} \nРуль:  {list_[0]} \nПробег:  {list_[1]}',
                    reply_markup=keyboards)





    # if c.data == 'Назад':
    #     bot.send_message(chat_id, f'Вы вернулись обратно', reply_markup=None)
    # elif c.data == 'Выйти':
    #     pass

    # bot.edit_message_text(chat_id=chat_id, messange_id=c.message.messange_id, text=f'{list_dict[index]}', reply_markup=None)
    # bot.send_message('', chat_id, reply_markup=None)

bot.polling()