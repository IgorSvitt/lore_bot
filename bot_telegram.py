from telebot import types, async_telebot
from bot_utils import lang_dict
from database_all_tables import Database, Tags, Fandoms, Users, Pairings
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = async_telebot.AsyncTeleBot(TOKEN)

db = Database()
us = Users()
tg = Tags()
fd = Fandoms()
pr = Pairings()


@bot.message_handler(commands=['start'])
async def send_start_message(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    first_name = message.from_user.first_name

    await us.add_users(chat_id, first_name)

    russian_button = types.InlineKeyboardButton(text="Русский 🇷🇺 ", callback_data=f"russian_{chat_id}")
    english_button = types.InlineKeyboardButton(text="English 🇬🇧 ", callback_data=f"english_{chat_id}")

    keyboard.add(russian_button, english_button)

    await bot.send_message(message.chat.id,
                           f"Привет, <b>{first_name}</b>! \n"
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


async def start_handler(call, language, language_dict):
    chat_id = call.message.chat.id
    texts = language_dict.get(language, language_dict['ru'])
    keyboard = types.InlineKeyboardMarkup()

    form_button = types.InlineKeyboardButton(text=texts['form'], callback_data=f"form_{chat_id}")
    finder_button = types.InlineKeyboardButton(text=texts['finder'], callback_data=f"finder_{chat_id}")
    favorites_button = types.InlineKeyboardButton(text=texts['favorites'], callback_data=f"favorites_{chat_id}")
    lore_button = types.InlineKeyboardButton(text=texts['favorites'], callback_data=f"lore_info_{chat_id}")

    keyboard.row(form_button)
    keyboard.row(finder_button)
    keyboard.row(favorites_button)
    keyboard.row(lore_button)
    await bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


async def form_handler(call, language, language_dict):
    chat_id = call.message.chat.id
    texts = language_dict.get(language, language_dict['ru'])

    keyboard = types.InlineKeyboardMarkup()
    choose_tag_button = types.InlineKeyboardButton(text=texts['choose_tag'], callback_data=f"tag_{chat_id}")
    choose_fandom_button = types.InlineKeyboardButton(text=texts['choose_fandom'], callback_data=f"fandom_{chat_id}")
    pairing_button = types.InlineKeyboardButton(text=texts['choose_pairings'],
                                                callback_data=f"choose_pairings_{chat_id}")
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_form_{chat_id}")
    keyboard.row(choose_tag_button)
    keyboard.row(choose_fandom_button)
    keyboard.row(back_button)
    keyboard.row(pairing_button)
    await bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


async def choose_tags(call, language, language_dict):
    tags = await tg.get_all_tags()
    tags_list = [item[0] for item in tags]
    texts = language_dict.get(language, language_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    tag_buttons = [types.InlineKeyboardButton(text=tag, callback_data=f"{tag}_{chat_id}")
                   for tag in tags_list]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_tags_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_tags_{chat_id}")
    keyboard.add(*tag_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)

    await bot.send_message(chat_id, texts['tags_message'], reply_markup=keyboard)


async def choose_fandom(call, language, language_dict):
    fandoms = await fd.get_all_fandoms()
    fandoms_list = [item[0] for item in fandoms]
    texts = language_dict.get(language, language_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    fandom_buttons = [types.InlineKeyboardButton(text=fandom, callback_data=f"{fandom}_{chat_id}")
                      for fandom in fandoms_list]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_tags_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_fandom_{chat_id}")

    keyboard.add(*fandom_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)

    await bot.send_message(chat_id, texts['fandoms_message'], reply_markup=keyboard)


async def choose_pairings(call, language, language_dict):
    pass


async def finder_handler(call, language, language_dict):
    texts = language_dict.get(language, language_dict['ru'])
    keyboard = types.InlineKeyboardMarkup()
    chat_id = call.chat.id
    like_button = types.InlineKeyboardButton(text=texts['like'], callback_data=f"like_{chat_id}")
    dislike_button = types.InlineKeyboardButton(text=texts['dislike'], callback_data=f"dislike_{chat_id}")
    keyboard.add(like_button, dislike_button)
    await bot.send_message(chat_id,
                           "Fanfinder это как Тиндер только для фанфиков. Выбери себе чтиво по душе!:\n",
                           reply_markup=keyboard)


async def add_users_tags_handler(call, chat_id):
    chosen_tag = call.data.split('_')[0]
    chosen_tag_id = await tg.get_tag_id(chosen_tag)
    user_tags = await us.get_all_users_tags(chat_id)
    if chosen_tag_id not in user_tags:
        await us.add_users_tags(chat_id, chosen_tag_id)
        await bot.answer_callback_query(call.id, text="Тег выбран (Tag is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Тег уже выбран (Tag has been already chosen)")


async def add_users_fandoms_handler(call, chat_id):
    chosen_fandom = call.data.split('_')[0]
    chosen_fandom_id = await fd.get_fandom_id(chosen_fandom)
    user_fandoms = await us.get_all_users_fandoms(chat_id)
    if chosen_fandom_id not in user_fandoms:
        await us.add_users_fandoms(chat_id, chosen_fandom_id)
        await bot.answer_callback_query(call.id, text="Фандом выбран (Fandom is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Фандом уже выбран (Fandom has been already chosen)")


async def is_call_startswith_tag():
    tags_list = await tg.get_all_tags()
    return lambda call: any(call.data.startswith(f"{tag}") for tag in tags_list)


async def is_call_startswith_fandom():
    fandoms_list = await fd.get_all_fandoms()
    return lambda call: any(call.data.startswith(f"{fandom}") for fandom in fandoms_list)


async def is_call_startswith_pairing():
    pairings_list = await pr.get_all_pairings()
    return lambda call: any(call.data.startswith(f"{pairing}") for pairing in pairings_list)


@bot.callback_query_handler(func=lambda call: call.data.startswith('russian_') or call.data.startswith('english_'))
async def call_language(call):
    chat_id = call.message.chat.id
    if call.data.startswith('english_'):
        await us.add_users_language(chat_id, 'en')
    else:
        await us.add_users_language(chat_id, 'ru')
    language_mode = await us.get_users_language(chat_id)
    await bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['chosen_language'])
    await start_handler(call, language_mode, lang_dict)


@bot.callback_query_handler(func=lambda call: call.data.startswith('form_'))
async def call_form(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('form_'):
        await form_handler(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('tag_'))
async def call_tag(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('tag_'):
        await choose_tags(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('fandom_'))
async def call_fandom(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('fandom_'):
        await choose_fandom(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_form_'))
async def call_back_form(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('back_form_'):
        await start_handler(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_tags_'))
async def call_back_tags(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('back_tags_'):
        await form_handler(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('clear_tags_'))
async def call_clear_tags(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('clear_tags_'):
        await bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['cleared'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('clear_fandoms_'))
async def call_clear_fandoms(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('clear_fandoms_'):
        await bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['cleared'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('finder_'))
async def call_finder(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('finder_'):
        await finder_handler(call, language_mode, lang_dict)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=is_call_startswith_tag())
async def call_choose_tags(call):
    chat_id = call.message.chat.id
    if call.data.startswith('choose_tags_'):
        await add_users_tags_handler(call, chat_id)


@bot.callback_query_handler(func=is_call_startswith_fandom())
async def call_choose_fandoms(call):
    chat_id = call.message.chat.id
    if call.data.startswith('choose_fandoms_'):
        await add_users_fandoms_handler(call, chat_id)


# admin штука, потом уберу
@bot.message_handler(func=lambda message: message.text.startswith('ТЕГИ'))
async def add_tag_admin(message):
    text = message.text
    tag_text = text.split('ТЕГИ', 1)[1].strip()
    for tag in tag_text.split():
        await tg.add_tag(tag)


@bot.message_handler(func=lambda message: message.text.startswith('ФАНДОМЫ'))
async def add_fd_admin(message):
    text = message.text
    fandom_text = text.split('ФАНДОМЫ', 1)[1].strip()
    for fandom in fandom_text.split():
        await fd.add_fandom(fandom)


@bot.message_handler(func=lambda message: message.text.startswith('ПЕЙРИНГИ'))
async def add_fd_admin(message):
    text = message.text
    pairing_text = text.split('ПЕЙРИНГИ', 1)[1].strip()
    pairing = pairing_text.split()
    for i in range(len(pairing) - 1):
        await pr.add_pairing(pairing[i], pairing_text[i + 1])
