import telebot
from telebot import types
from bot_utils import lang_dict

TOKEN = ""
language_mode = 'ru'
user_dict = {}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_start_message(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()

    russian_button = types.InlineKeyboardButton(text="Русский 🇷🇺 ", callback_data=f"russian_{chat_id}")
    english_button = types.InlineKeyboardButton(text="English 🇬🇧 ", callback_data=f"english_{chat_id}")

    keyboard.add(russian_button, english_button)

    bot.send_message(message.chat.id,
                     f"Привет, <b>{message.from_user.first_name}</b>! \n"
                     "Я бот компании LORE. \n"
                     "Я твой персональный помощник по поиску фанфиков, которые подходят именно тебе!"
                     "В начале, тебе нужно выбрать язык общения :)"
                     "Нажми на тот язык, на котором хочешь продолжить \n"
                     "\n"
                     f"Hi, <b>{message.from_user.first_name}</b>! \n"
                     "I am a bot of the LORE company.\n"
                     " I am your personal assistant to find the fanfiction that is right for you!"
                     "In the beginning, you need to choose the language of communication :)"
                     "Click on the language you want to continue in\n",
                     parse_mode='html',
                     reply_markup=keyboard)


def start_handler(call, language, language_dict):
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()

    texts = language_dict.get(language, language_dict['ru'])

    form_button = types.InlineKeyboardButton(text=texts['form'], callback_data=f"form_{chat_id}")
    finder_button = types.InlineKeyboardButton(text=texts['finder'], callback_data=f"finder_{chat_id}")
    favorites_button = types.InlineKeyboardButton(text=texts['favorites'], callback_data=f"favorites_{chat_id}")
    lore_button = types.InlineKeyboardButton(text=texts['favorites'], callback_data=f"lore_info_{chat_id}")

    keyboard.row(form_button)
    keyboard.row(finder_button)
    keyboard.row(favorites_button)
    keyboard.row(lore_button)
    bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


def form_handler(call, language, language_dict):
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()

    texts = language_dict.get(language, language_dict['ru'])
    choose_tag_button = types.InlineKeyboardButton(text=texts['choose_tag'], callback_data=f"tag_{chat_id}")
    choose_fandom_button = types.InlineKeyboardButton(text=texts['choose_fandom'], callback_data=f"fandom_{chat_id}")
    pairing_button = types.InlineKeyboardButton(text=texts['choose_pairings'],
                                                callback_data=f"choose_pairings_{chat_id}")
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_form_{chat_id}")
    keyboard.row(choose_tag_button)
    keyboard.row(choose_fandom_button)
    keyboard.row(back_button)
    keyboard.row(pairing_button)
    bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


def choose_tags(call, language, language_dict):
    texts = language_dict.get(language, language_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    tag_buttons = [types.InlineKeyboardButton(text=tag, callback_data=f"{tag.lower()}_{chat_id}")
                   for tag in language_dict['tags']]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_tags_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_tags_{chat_id}")
    keyboard.add(*tag_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)
    bot.send_message(chat_id, texts['tags_message'], reply_markup=keyboard)


def choose_fandom(call, language, language_dict):
    texts = language_dict.get(language, language_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    fandom_buttons = [types.InlineKeyboardButton(text=fandom, callback_data=f"{fandom.lower()}_{chat_id}")
                      for fandom in language_dict['fandoms']]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_tags_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_fandom_{chat_id}")
    keyboard.add(*fandom_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)
    bot.send_message(chat_id, texts['fandoms_message'], reply_markup=keyboard)


def choose_pairings(call, language, language_dict):
    pass


def finder_handler(call, language, language_dict):
    texts = language_dict.get(language, language_dict['ru'])
    keyboard = types.InlineKeyboardMarkup()
    chat_id = call.chat.id
    like_button = types.InlineKeyboardButton(text=texts['like'], callback_data=f"like_{chat_id}")
    dislike_button = types.InlineKeyboardButton(text=texts['dislike'], callback_data=f"dislike_{chat_id}")
    keyboard.add(like_button, dislike_button)
    bot.send_message(chat_id,
                     "Fanfinder это как Тиндер только для фанфиков. Выбери себе чтиво по душе!:\n",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global language_mode
    chat_id = call.message.chat.id
    user_tags = user_dict.get(chat_id, {'selected_tags': []})
    user_fandoms = user_dict.get(chat_id, {'selected_fandoms': []})

    if call.data.startswith('russian_'):
        language_mode = 'ru'
        start_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id, text="Выбран русский язык")
    elif call.data.startswith('english_'):
        language_mode = 'en'
        start_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id, text="The chosen language is English")
    elif call.data.startswith('form_'):
        form_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('tag_'):
        choose_tags(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('fandom_'):
        choose_fandom(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('back_form_'):
        start_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('back_tags_'):
        form_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('clear_tags_'):
        user_tags['selected_tags'] = []
        bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['cleared_tags'])
    elif call.data.startswith('clear_fandom_'):
        user_tags['selected_fandoms'] = []
        bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['cleared_tags'])
    elif call.data.startswith('finder_'):
        finder_handler(call, language_mode, lang_dict)
        bot.answer_callback_query(call.id)
    for tag in lang_dict['tags']:
        if call.data.startswith(f"{tag.lower()}_"):
            chosen_tag = call.data.split('_')[0]
            if chosen_tag.lower() not in user_tags['selected_tags']:
                if chat_id in user_dict:
                    user_dict[chat_id]['selected_tags'].append(chosen_tag.lower())
                    print(user_dict)
                else:
                    user_dict[chat_id] = {'selected_tags': [chosen_tag.lower()],
                                          'selected_fandoms': []}
                    print(user_dict)
                bot.answer_callback_query(call.id, text="Тег выбран (Tag is chosen)")
            else:
                bot.answer_callback_query(call.id, text="Тег уже выбран (Tag has been already chosen)")
                for fandom in lang_dict['fandoms']:
                    if call.data.startswith(f"{fandom.lower()}_"):
                        chosen_fandom = call.data.split('_')[0]
                        if chosen_fandom.lower() not in user_fandoms['selected_fandoms']:
                            if chat_id in user_dict:
                                user_dict[chat_id]['selected_fandoms'].append(chosen_fandom.lower())
                                print(user_dict)
                            else:
                                user_dict[chat_id] = {'selected_tags': [],
                                                      'selected_fandoms': [chosen_fandom.lower()]}
                                print(user_dict)
                            bot.answer_callback_query(call.id, text="Фан выбран (Fandom is chosen)")
                        else:
                            bot.answer_callback_query(call.id, text="Тег уже выбран (Fandom has been already chosen)")

            bot.polling()
