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


@bot.message_handler(command=['open_character'])
def open_character(message):
    character_name = message.text
    save_path = './characters/' + message.from_user.username + '.json'

    with open(save_path, encoding=ENCODING) as save_file:
        characters = json.load(save_file)

    character = [character for character in characters if character['name'] == character_name]

    if not character:
        bot.send_message(message.from_user.id, text='Нет такого персонажа')
        stop(message)
    else:
        def ask_formula(message, character):
            def change_stat(message, character, stat):
                try:
                    d = int(message.text)
                except:
                    print(message.text, stat)
                    bot.send_message(message.from_user.id, 'Введите число')
                    bot.register_next_step_handler(message, change_stat, character, stat)

                character.js['resources'][stat] += d
                character = Character(character.file_name, character.js).save()

                bot.send_message(CHAT_ID, f'{character.name} изменил(а) свой показатель {stat}, на "{d}"')

                char_menu(message, character.js)

            bot.send_message(message.from_user.id, 'Как изменить показатель?', reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(message, change_stat, character, message.text)

        def char_menu(message, character_js):
            markup = types.ReplyKeyboardMarkup()
            markup.row(types.KeyboardButton('здоровье'))
            markup.row(types.KeyboardButton('выносливость'))
            markup.row(types.KeyboardButton('рассудок'))
            markup.row(types.KeyboardButton('воля'))

            character = Character(message.from_user.username, character_js)
            bot.send_message(message.from_user.id, character.to_sting(), parse_mode='html', reply_markup=markup)

            bot.register_next_step_handler(message, ask_formula, character)

        char_menu(message, character[0])

@bot.message_handler(commands=['character_list'])
def character_list(message):
    save_path = './characters/' + message.from_user.username + '.json'

    if os.path.exists(save_path):
        markup = types.ReplyKeyboardMarkup()
        with open(save_path, encoding=ENCODING) as save_file:
            characters = json.load(save_file)
            for character in characters:
                create_char_button = types.KeyboardButton(character['name'])
                markup.row(create_char_button)
        ans = bot.send_message(message.from_user.id, "Выберите вашего персонажа:", reply_markup=markup)
        bot.register_next_step_handler(ans, open_character)

    else:
        markup = types.ReplyKeyboardMarkup()
        create_char_button = types.KeyboardButton('Создать персонажа')
        markup.row(create_char_button)

        ans = bot.send_message(message.from_user.id, "У Вас пока нет созданных персонажей, создать?",
                               reply_markup=markup)

        def check_ans(message):
            if message.text == 'Создать персонажа':
                bot.send_message(message.from_user.id, 'А жаренных гвоздей не хочешь?')
                bot.register_next_step_handler(message, stop)
            else:
                bot.register_next_step_handler(message, stop)

        bot.register_next_step_handler(ans, check_ans)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    name = message.from_user.username
    markup = types.ReplyKeyboardMarkup()

    open_char_button = types.KeyboardButton('Открыть персонажа')
    markup.row(open_char_button)

    ans = bot.send_message(message.from_user.id, f"Здравствуй, {name}", parse_mode='html', reply_markup=markup)

    bot.register_next_step_handler(ans, character_list)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.from_user.id, "", reply_markup=ReplyKeyboardRemove())


bot.infinity_polling()
