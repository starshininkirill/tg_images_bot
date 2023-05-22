from telebot import TeleBot, types
from test_utils import *

stages = ['menu', 'choise', 'result']

stage = stages[0]


@bot.message_handler(commands=['start'])
def start(message):
    stage = stages[0]
    bot.send_message(message.chat.id, 'Это бот для обработки фотографий, отаправь изображение чтобы начать')


@bot.message_handler(content_types=['text'])
def test(message):
    global stage
    if stage == 'menu':
        bot.send_message(message.chat.id, 'Отправте картинку, чтобы бот сделал для неё рамку')
    elif stage == 'choise':
        bot.send_message(message.chat.id, 'Нажмите на кнопку')


@bot.message_handler(content_types=['document'])
def document(message):
    global stage
    user_id = message.chat.id

    if stage == 'menu':
        image_name = download_photo(message, 'document')

        kb = types.InlineKeyboardMarkup(row_width=3)
        # btn_1 = types.InlineKeyboardButton(text='1', callback_data=f'{image_name}|1')
        btn_2 = types.InlineKeyboardButton(text='2', callback_data=f'{image_name}|2')
        btn_3 = types.InlineKeyboardButton(text='3', callback_data=f'{image_name}|3')
        kb.add(btn_2, btn_3)
        bot.send_media_group(message.chat.id, [
                                               # types.InputMediaPhoto(open('images/sourse/ram_1.png', 'rb')),
                                               types.InputMediaPhoto(open('images/sourse/ram_2.png', 'rb')),
                                               types.InputMediaPhoto(open('images/sourse/ram_3.png', 'rb'))])
        bot.send_message(message.chat.id, 'Выберите рамку для фото', reply_markup=kb)

        stage = 'choise'


@bot.message_handler(content_types=['photo'])
def photo(message):
    global stage
    user_id = message.chat.id

    if stage == 'menu':
        image_name = download_photo(message, 'photo')

        kb = types.InlineKeyboardMarkup(row_width=3)
        # btn_1 = types.InlineKeyboardButton(text='1', callback_data=f'{image_name}|1')
        btn_2 = types.InlineKeyboardButton(text='2', callback_data=f'{image_name}|2')
        btn_3 = types.InlineKeyboardButton(text='3', callback_data=f'{image_name}|3')
        kb.add(btn_2, btn_3)
        bot.send_media_group(message.chat.id, [
                                               # types.InputMediaPhoto(open('images/sourse/ram_1.png', 'rb')),
                                               types.InputMediaPhoto(open('images/sourse/ram_2.png', 'rb')),
                                               types.InputMediaPhoto(open('images/sourse/ram_3.png', 'rb'))])
        bot.send_message(message.chat.id, 'Выберите рамку для фото', reply_markup=kb)

        stage = 'choise'


@bot.callback_query_handler(func=lambda call: True)
def choise(call):
    user_id = call.from_user.id
    global stage
    bot.answer_callback_query(call.id)

    if stage == 'choise':
        if call.data.split('|')[1] == '1':
            image_name = call.data.split('|')[0]
            bot.send_message(call.message.chat.id, 'Вы выбрали 1 рамку')
            photo_name = reformat_image(image_name, user_id, '1')
            bot.send_photo(call.message.chat.id, open(photo_name, 'rb'))
            stage = 'menu'
        elif call.data.split('|')[1] == '2':
            image_name = call.data.split('|')[0]
            bot.send_message(call.message.chat.id, 'Вы выбрали 2 рамку')
            photo_name = reformat_image(image_name, user_id, '2')
            bot.send_photo(call.message.chat.id, open(photo_name, 'rb'))
            stage = 'menu'
        elif call.data.split('|')[1] == '3':
            image_name = call.data.split('|')[0]
            bot.send_message(call.message.chat.id, 'Вы выбрали 3 рамку')
            photo_name = reformat_image(image_name, user_id, '3')
            bot.send_photo(call.message.chat.id, open(photo_name, 'rb'))
            stage = 'menu'
    else:
        bot.send_message(call.message.chat.id, 'Сначала отправьте фото')

bot.infinity_polling()