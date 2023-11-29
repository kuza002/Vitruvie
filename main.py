import os
import json
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove
from character import Character

ENCODING = 'utf-8'

BOT_TOKEN = "6811215765:AAGri2LdNJ2LTH1uyLcaRm_F1Z1HukHnATo"
CHAT_ID = '-4028822764'

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['create_character'])
def create_character(message):
    bot.send_message(message.from_user.id, "А жаренных гвоздей не хочешь?")


def char_menu(user, character_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('здоровье', callback_data='change_здоровье_' + character_name))
    markup.add(types.InlineKeyboardButton('выносливость', callback_data='change_выносливость_' + character_name))
    markup.add(types.InlineKeyboardButton('рассудок', callback_data='change_рассудок_' + character_name))
    markup.add(types.InlineKeyboardButton('воля', callback_data='change_воля_' + character_name))

    markup.row(
        types.InlineKeyboardButton('Отдых', callback_data=character_name + '_rest'),
        types.InlineKeyboardButton('Навыки', callback_data=character_name + '_skills'),
        types.InlineKeyboardButton('Бросок', callback_data=character_name + '_roll')
    )

    markup.add(types.InlineKeyboardButton('Главное меню', callback_data='go_home'))

    characters_js = get_list_of_characters(user.username)
    character_js = find_character_by_name(character_name, characters_js)

    character = Character(user.username, character_js)
    bot.send_message(user.id, character.to_sting(), parse_mode='html', reply_markup=markup)


def get_list_of_characters(username):
    save_path = './characters/' + username + '.json'
    if os.path.exists(save_path):
        with open(save_path, encoding=ENCODING) as save_file:
            characters_js = json.load(save_file)
        return characters_js
    else:
        return []


def find_character_by_name(name, characters_js):
    for character_js in characters_js:
        if character_js['name'] == name:
            return character_js
    return None


def character_list(username, user_id):
    characters_js = get_list_of_characters(username)

    # if save file is existed then create button with all characters
    if characters_js:
        markup = types.InlineKeyboardMarkup()

        for character in characters_js:
            create_char_button = types.InlineKeyboardButton(character['name'],
                                                            callback_data="name_" + character['name'])
            markup.row(create_char_button)

        bot.send_message(user_id, "Выберите вашего персонажа:", reply_markup=markup)

    # else create character or back to main menu
    else:
        markup = types.InlineKeyboardMarkup()
        create_char_button = types.InlineKeyboardButton('Да', callback_data='create_character')
        go_main_menu_button = types.InlineKeyboardButton('Нет', )
        markup.row(create_char_button, go_main_menu_button)

        ans = bot.send_message(user_id, "У Вас пока нет созданных персонажей, создать?",
                               reply_markup=markup)

        def check_ans(message):
            if message.text == 'Создать персонажа':
                bot.send_message(message.from_user.id, 'А жаренных гвоздей не хочешь?')
                bot.register_next_step_handler(message, stop)
            else:
                bot.register_next_step_handler(message, stop)

        bot.register_next_step_handler(ans, check_ans)


def change_stat(message, character, stat):
    try:
        d = int(message.text)
    except:
        bot.send_message(message.from_user.id, 'Введите число')
        bot.register_next_step_handler(message, change_stat, character, stat)

    valid_d = character.add_to_stat(stat, d)

    bot.send_message(CHAT_ID,
                     f'{character.name} сделал(а) свой показатель {stat} равным "{valid_d}", добавив к нему {d}')

    char_menu(message.from_user, character.name)


@bot.callback_query_handler(func=lambda c: c.data[-10:] == '_character' or c.data == 'go_home')
def main_menu_distributor(callback_data):
    action = callback_data.data[:-10]

    if action == 'open':
        character_list(callback_data.from_user.username, callback_data.from_user.id)
    elif callback_data.data == 'go_home':
        main_menu(callback_data)
    else:
        bot.send_message(callback_data.from_user.username, 'Данный функционал не реализован')
        main_menu(callback_data)


@bot.message_handler(commands=['start', 'hello'])
def main_menu(message):
    name = message.from_user.username

    # Init buttons in menu
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Открыть персонажа', callback_data='open_character'))
    markup.add(types.InlineKeyboardButton('Создать персонажа', callback_data='create_character'))
    markup.add(types.InlineKeyboardButton('Удалить персонажа', callback_data='delete_character'))

    #
    ans = bot.send_message(message.from_user.id, f"Здравствуй, {name}", parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data[:4] == 'name')
def open_character(callback):
    character_name = callback.data[5:]

    characters_js = get_list_of_characters(callback.from_user.username)
    character_js = find_character_by_name(character_name, characters_js)

    if characters_js:
        char_menu(callback.from_user, character_js['name'])
    else:
        bot.send_message(callback.from_user.id, text='Нет такого персонажа')
        main_menu(callback)


@bot.callback_query_handler(func=lambda c: c.data.split('_')[0] == 'change')
def ask_formula(callback_query):
    data = callback_query.data.split('_')

    characters_js = get_list_of_characters(callback_query.from_user.username)
    character_js = find_character_by_name(data[2], characters_js)

    character = Character(callback_query.from_user.username, character_js)

    bot.send_message(callback_query.from_user.id, 'Как изменить показатель?', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(callback_query.message, change_stat, character, data[1])


@bot.callback_query_handler(func=lambda c: c.data.split('_')[1] == 'rest')
def rest_all(callback_query):
    character_name = callback_query.data.split('_')[0]
    characters_js = get_list_of_characters(callback_query.from_user.username)
    character_js = find_character_by_name(character_name, characters_js)

    bot.send_message(CHAT_ID, f'{character_name} отдохнул(а) и восстановил все рессурсы')

    del character_js['resources']
    Character(callback_query.from_user.username, character_js).save()
    char_menu(callback_query.from_user, character_name)


@bot.callback_query_handler(func=lambda c: c.data.split('_')[0] == 'skill' and c.data.split('_')[1].isdigit())
def show_skill(callback_query):
    data = callback_query.data.split('_')
    characters_js = get_list_of_characters(callback_query.from_user.username)
    character_js = find_character_by_name(data[2], characters_js)

    number = 0
    for skill_type, skills in character_js['skills'].items():
        for titel, disc in skills.items():
            number += 1
            if str(number) == data[1]:
                bot.send_message(CHAT_ID, f'<b>{character_js['name']}</b>\n'
                                          f'<i>Исспользует {skill_type[:-1].lower()+'й'} навык "{titel}"</i>\n{''.join(disc)}',
                                 parse_mode='html')

@bot.callback_query_handler(func=lambda c: c.data.split('_')[1] == 'skills')
def get_skills(callback_query):
    character_name = callback_query.data.split('_')[0]
    characters_js = get_list_of_characters(callback_query.from_user.username)
    character_js = find_character_by_name(character_name, characters_js)

    text = ''
    number = 0
    for skill_type, skills in character_js['skills'].items():
        text += f'<b>{skill_type}</b>\n'
        for title, disc in skills.items():
            number += 1
            text += f'{number}.{title}'
            text += f'\n\t<i>{''.join(disc)}</i>\n'
        text += '\n\n'

    markup = types.InlineKeyboardMarkup()
    buttons = []
    for i in range(1, number+1):
        buttons.append(types.InlineKeyboardButton(str(i), callback_data='skill_'+str(i)+'_'+character_name))

    markup.row(*buttons)
    markup.add(types.InlineKeyboardButton("Назад", callback_data='name_'+character_name))

    bot.send_message(callback_query.from_user.id, text, parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.split('_')[1] == 'roll')
def roll():
    pass


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.from_user.id, "", reply_markup=ReplyKeyboardRemove())


bot.infinity_polling()
