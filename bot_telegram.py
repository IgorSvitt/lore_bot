from telebot import types, async_telebot
from bot_utils import lang_dict, process_post
from database_all_tables import Database, Tags, Fandoms, Users, Pairings, Relationships, Fanfiction, Authors
from RecSys import RecommendationSystem
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = async_telebot.AsyncTeleBot(TOKEN)

db = Database()
us = Users()
au = Authors()
tg = Tags()
fd = Fandoms()
pr = Pairings()
rl = Relationships()
ff = Fanfiction()
rs = RecommendationSystem()


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


@bot.message_handler(commands=['help'])
async def send_start_message(message):
    await bot.send_message(message.chat.id,
                           "Some info about LORE\n",
                           parse_mode='html')


async def start_handler(call, language):
    chat_id = call.message.chat.id
    texts = lang_dict.get(language, lang_dict['ru'])
    keyboard = types.InlineKeyboardMarkup()

    form_button = types.InlineKeyboardButton(text=texts['form'], callback_data=f"form_{chat_id}")
    finder_button = types.InlineKeyboardButton(text=texts['finder'], callback_data=f"finder_{chat_id}")
    favorites_button = types.InlineKeyboardButton(text=texts['favorites'], callback_data=f"favorites_{chat_id}")
    lore_button = types.InlineKeyboardButton(text='❓', callback_data=f"lore_info_{chat_id}")

    keyboard.row(form_button)
    keyboard.row(finder_button)
    keyboard.row(favorites_button)
    keyboard.row(lore_button)
    await bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


async def form_handler(call, language):
    chat_id = call.message.chat.id
    texts = lang_dict.get(language, lang_dict['ru'])

    keyboard = types.InlineKeyboardMarkup()
    choose_tag_button = types.InlineKeyboardButton(text=texts['choose_tag'], callback_data=f"tag_{chat_id}")
    choose_fandom_button = types.InlineKeyboardButton(text=texts['choose_fandom'], callback_data=f"fandom_{chat_id}")
    pairing_button = types.InlineKeyboardButton(text=texts['choose_pairings'],
                                                callback_data=f"pairing_{chat_id}")
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_start_{chat_id}")
    keyboard.row(choose_tag_button)
    keyboard.row(choose_fandom_button)
    keyboard.row(back_button)
    keyboard.row(pairing_button)
    await bot.send_message(chat_id, texts['activity'], reply_markup=keyboard)


async def choose_tags(call, language):
    tags = await tg.get_all_tags()
    tags_list = [item[0] for item in tags]
    texts = lang_dict.get(language, lang_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    tag_buttons = [types.InlineKeyboardButton(text=tag, callback_data=f"choose_tags_{tag}_{chat_id}")
                   for tag in tags_list]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_form_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_tags_{chat_id}")
    keyboard.add(*tag_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)

    await bot.send_message(chat_id, texts['tags_message'], reply_markup=keyboard)


async def choose_fandom(call, language):
    fandoms = await fd.get_all_fandoms()
    fandoms_list = [item[0] for item in fandoms]
    texts = lang_dict.get(language, lang_dict['ru'])
    chat_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    fandom_buttons = [types.InlineKeyboardButton(text=fandom, callback_data=f"choose_fandoms_{fandom}_{chat_id}")
                      for fandom in fandoms_list]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_form_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_fandoms_{chat_id}")

    keyboard.add(*fandom_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)

    await bot.send_message(chat_id, texts['fandoms_message'], reply_markup=keyboard)


async def choose_pairing(call, language):
    chat_id = call.message.chat.id
    texts = lang_dict.get(language, lang_dict['ru'])

    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_form_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_common_pairings_{chat_id}")
    keyboard.row(back_button)
    chosen_fandoms_id = await us.get_all_users_fandoms(chat_id)
    if chosen_fandoms_id:
        chosen_fandoms_id_list = [item[0] for item in chosen_fandoms_id]
        chosen_fandoms_list = [await fd.get_fandom_by_id(fd_id) for fd_id in chosen_fandoms_id_list]
        chosen_fandoms_buttons = [
            types.InlineKeyboardButton(text=chosen_fandom,
                                       callback_data=f"choose_pairings_fandoms_{chosen_fandom}_{chat_id}")
            for chosen_fandom in chosen_fandoms_list]
        keyboard.add(*chosen_fandoms_buttons)
        await bot.send_message(chat_id, texts['pairings_fandoms_message'], reply_markup=keyboard)
    else:
        common_pairings = await rl.get_all_relationships()
        common_pairings_buttons = [types.InlineKeyboardButton
                                   (text=relationship[0],
                                    callback_data=f"choose_pairings_common_{relationship[0]}_{chat_id}")
                                   for relationship in common_pairings]
        for button in common_pairings_buttons:
            keyboard.row(button)
        keyboard.row(clear_button)
        await bot.send_message(chat_id, texts['pairings_common_message'], reply_markup=keyboard)


async def users_pairings_handler(call, language, chat_id):
    keyboard = types.InlineKeyboardMarkup()
    texts = lang_dict.get(language, lang_dict['ru'])
    chosen_fandom = call.data.split('_')[3]
    chosen_fandom_id = await fd.get_fandom_id(chosen_fandom)
    pairings_in_fandom = await pr.get_pairings_by_fandom(chosen_fandom_id[0])
    available_pairings_buttons = [types.InlineKeyboardButton
                                  (text=available_pairing[0],
                                   callback_data=f"choose_pairings_user_{available_pairing[0]}_{chat_id}")
                                  for available_pairing in pairings_in_fandom]
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_pairings_{chat_id}")
    clear_button = types.InlineKeyboardButton(text=texts['clear'], callback_data=f"clear_pairings_{chat_id}")
    keyboard.add(*available_pairings_buttons)
    keyboard.add(back_button)
    keyboard.add(clear_button)
    await bot.send_message(chat_id, texts['pairings_message'], reply_markup=keyboard)


async def finder_handler(language, chat_id):
    texts = lang_dict.get(language, lang_dict['ru'])
    keyboard = types.InlineKeyboardMarkup()
    find_ff_button = types.InlineKeyboardButton(text=texts['find_ff'], callback_data=f"find_ff_{chat_id}")
    lore_button = types.InlineKeyboardButton(text='❓', callback_data=f"lore_info_{chat_id}")
    back_button = types.InlineKeyboardButton(text=texts['back'], callback_data=f"back_start_{chat_id}")
    keyboard.add(find_ff_button, lore_button)
    keyboard.row(back_button)
    await bot.send_message(chat_id, texts['finder_greeting'], reply_markup=keyboard)


async def finder_recommend_handler(language, chat_id):
    texts = lang_dict.get(language, lang_dict['ru'])
    recommendation = await rs.rec_sys()
    ffid = recommendation[0]
    keyboard = types.InlineKeyboardMarkup()
    like_button = types.InlineKeyboardButton(text=texts['like'], callback_data=f"find_ff_like_{ffid}_{chat_id}")
    dislike_button = types.InlineKeyboardButton(text=texts['dislike'],
                                                callback_data=f"find_ff_dislike_{ffid}_{chat_id}")
    keyboard.add(like_button, dislike_button)
    await bot.send_message(chat_id, recommendation, reply_markup=keyboard)


async def finder_narrow_tags_handler(language, chat_id, ff_id, action):
    texts = lang_dict.get(language, lang_dict['ru'])
    msg = texts[action + '_' + 'message']
    narrow_tags_ids = await ff.get_narrow_tag_id_by_ff_id(ff_id)
    narrow_tags = [await tg.get_narrow_tag_name_by_id(nt_id) for nt_id in narrow_tags_ids]
    pairs = zip(narrow_tags_ids, narrow_tags)
    result_dict = dict(pairs)
    result_dict["action"] = action
    narrow_tags_buttons = [types.InlineKeyboardButton
                           (text=narrow_tag,
                            callback_data=f"nrw_tg_o_{narrow_tag}_{chat_id}")
                           for narrow_tag in narrow_tags]
    all_button = types.InlineKeyboardButton(text=texts['all'],
                                            callback_data="nrw_tg_a_"
                                                          f"{result_dict}_{chat_id}")
    skip_button = types.InlineKeyboardButton(text=texts['skip'],
                                             callback_data=f"nrw_tg_s_{chat_id}")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*narrow_tags_buttons)
    keyboard.row(all_button)
    keyboard.row(skip_button)
    await bot.send_message(chat_id, msg, reply_markup=keyboard)


async def add_users_tags_handler(call, chat_id):
    chosen_tag = call.data.split('_')[2]
    chosen_tag_id = await tg.get_tag_id(chosen_tag)
    user_tags = await us.get_all_users_tags(chat_id)
    if not any(chosen_tag_id in t for t in user_tags):
        await us.add_users_tags(chat_id, chosen_tag_id)
        await bot.answer_callback_query(call.id, text="Тег выбран (Tag is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Тег уже выбран (Tag has been already chosen)")


async def add_users_fandoms_handler(call, chat_id):
    chosen_fandom = call.data.split('_')[2]
    chosen_fandom_id = await fd.get_fandom_id(chosen_fandom)
    user_fandoms = await us.get_all_users_fandoms(chat_id)
    if chosen_fandom_id not in [t for t in user_fandoms]:
        await us.add_users_fandoms(chat_id, chosen_fandom_id)
        await bot.answer_callback_query(call.id, text="Фандом выбран (Fandom is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Фандом уже выбран (Fandom has been already chosen)")


async def add_users_pairings(call, chat_id):
    chosen_pairing = call.data.split('_')[3]
    chosen_pairing_id = await pr.get_pairing_id(chosen_pairing)
    user_pairings = await us.get_all_users_pairings(chat_id)
    if chosen_pairing_id not in user_pairings:
        await us.add_users_pairings(chat_id, chosen_pairing_id)
        await bot.answer_callback_query(call.id, text="Пейринг выбран (Pairing is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Пейринг уже выбран (Pairing has been already chosen)")


async def add_users_relationships(call, chat_id):
    chosen_relationship = call.data.split('_')[3]
    chosen_relationship_id = await rl.get_relationship_id(chosen_relationship)
    user_relationships = await us.get_all_users_relationships(chat_id)
    if chosen_relationship_id not in user_relationships:
        await us.add_users_relationships(chat_id, chosen_relationship_id)
        await bot.answer_callback_query(call.id, text="Тип отношений выбран (Relationship type is chosen)")
    else:
        await bot.answer_callback_query(call.id, text="Тип отношений уже выбран (Relationship type has been already "
                                                      "chosen)")


@bot.callback_query_handler(func=lambda call: call.data.startswith('russian_') or call.data.startswith('english_'))
async def call_language(call):
    chat_id = call.message.chat.id
    if call.data.startswith('english_'):
        await us.add_users_language(chat_id, 'en')
    else:
        await us.add_users_language(chat_id, 'ru')
    language_mode = await us.get_users_language(chat_id)
    await bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['chosen_language'])
    await start_handler(call, language_mode)


@bot.callback_query_handler(func=lambda call: call.data.startswith('form_'))
async def call_form(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('form_'):
        await form_handler(call, language_mode)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('tag_'))
async def call_tag(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('tag_'):
        await choose_tags(call, language_mode)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('fandom_'))
async def call_fandom(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('fandom_'):
        await choose_fandom(call, language_mode)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('pairing_'))
async def call_pairing(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('pairing_'):
        await choose_pairing(call, language_mode)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_'))
async def call_back_start(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('back_start_'):
        await start_handler(call, language_mode)
    elif call.data.startswith('back_form_'):
        await form_handler(call, language_mode)
    elif call.data.startswith('back_pairings'):
        await choose_pairing(call, language_mode)
    await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('clear_'))
async def call_clear_tags(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('clear_tags_'):
        await us.delete_users_tags_by_chat_id(chat_id)
    elif call.data.startswith('clear_fandoms_'):
        users_fandoms = await us.get_all_users_fandoms(chat_id)
        for fandom in users_fandoms:
            await us.delete_users_pairings_by_chat_id_fandom(fandom, chat_id)
        await us.delete_users_fandoms_by_chat_id(chat_id)
    elif call.data.startswith('clear_pairings_'):
        await us.delete_users_pairings_by_chat_id(chat_id)
    elif call.data.startswith('clear_common_pairings'):
        await us.delete_users_relationships_by_chat_id(chat_id)
    await bot.answer_callback_query(call.id, text=lang_dict.get(language_mode, lang_dict['ru'])['cleared'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('finder_'))
async def call_finder(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('finder_'):
        await finder_handler(language_mode, chat_id)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('nrw_tg_'))
async def call_choose_narrow_tags(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('nrw_tg_'):
        if call.data.startswith('nrw_tg_o_'):
            narrow_tag = call.data.split('_')[3]
            narrow_tag_id = await tg.get_narrow_tag_id(narrow_tag)
            tag_id = await tg.get_tag_id_by_narrow_tag(narrow_tag_id)
            await tg.add_narrow_tag(narrow_tag, tag_id)  # отдельную функцию обработчик action передается
            await us.add_users_narrow_tags(chat_id, narrow_tag_id) # отдельную функцию обработчик action
        elif call.data.startswith('nrw_tg_a_'):
            narrow_tags = call.data.split('_')[3]
            for key, value in narrow_tags.items():
                narrow_tag_id = await tg.get_narrow_tag_id(key)
                tag_id = await tg.get_tag_id_by_narrow_tag(narrow_tag_id)
                await tg.add_narrow_tag(value, tag_id)  # отдельную функцию обработчик action передается
                await us.add_users_narrow_tags_disliked(chat_id, narrow_tag_id) # отдельную функцию обработчик action
        await finder_recommend_handler(language_mode, chat_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_tags_'))
async def call_choose_tags(call):
    chat_id = call.message.chat.id
    if call.data.startswith('choose_tags_'):
        await add_users_tags_handler(call, chat_id)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_fandoms_'))
async def call_choose_fandoms(call):
    chat_id = call.message.chat.id
    if call.data.startswith('choose_fandoms_'):
        await add_users_fandoms_handler(call, chat_id)
        await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_pairings_'))
async def call_choose_pairings(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    if call.data.startswith('choose_pairings_fandoms_'):
        await users_pairings_handler(call, language_mode, chat_id)
    elif call.data.startswith('choose_pairings_user_'):
        await add_users_pairings(call, chat_id)
    elif call.data.startswith('choose_pairings_common_'):
        await add_users_relationships(call, chat_id)
    await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lore_info_'))
async def send_help_info(call):
    await bot.send_message(call.message.chat.id,
                           "lore info")
    await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('find_ff_'))
async def call_finder(call):
    chat_id = call.message.chat.id
    language_mode = await us.get_users_language(chat_id)
    action = call.data.split('_')[2]
    ff_id = call.data.split('_')[3]
    print(ff_id, action)
    if call.data.startswith('find_ff_'):
        if call.data.startswith('find_ff_like_'):
            await us.add_users_preferences(chat_id, 1, ff_id)
        elif call.data.startswith('find_ff_dislike_'):
            await us.add_users_preferences(chat_id, 0, ff_id)
        await bot.answer_callback_query(call.id, 'Ваши предпочтения учтены (Your preferences are taken into account)')
        await finder_narrow_tags_handler(language_mode, chat_id, ff_id, action)


@bot.channel_post_handler(func=lambda message: 'telegra.ph' in message.text.lower())
async def handle_all_messages(message):
    content = message.text
    if 'telegra.ph' in content.lower():
        (title, author, relationship, fandom, tags, rating,
         status, size, description, pairings, url) = await process_post(content)
        await au.add_author(author)
        au_id = await au.get_author_id(author)
        await ff.add_fanfiction(title, rating, size, status, url, description, au_id)
        ff_id = await ff.get_fanfiction_id(title)
        await rl.add_relationship(relationship)
        rel_id = await rl.get_relationship_id(relationship)
        await ff.add_fanfiction_relationship(ff_id, rel_id)
        await fd.add_fandom(fandom)
        fd_id = await fd.get_fandom_id(fandom)
        await ff.add_fanfiction_fandom(ff_id, fd_id)
        for pairing in pairings:
            await pr.add_pairing(pairing, fd_id)
            pr_id = await pr.get_pairing_id(pairing)
            await ff.add_fanfiction_pairing(ff_id, pr_id)
        for pair in tags:
            category = pair[0]
            tags_list = pair[1]
            await tg.add_tag(category)
            tg_id = await tg.get_tag_id(category)
            await ff.add_fanfiction_tag(ff_id, tg_id)
            for narrow_tag in tags_list:
                await tg.add_narrow_tag(narrow_tag, tg_id)
                n_tg_id = await tg.get_narrow_tag_id(narrow_tag)
                await ff.add_fanfiction_narrow_tag(ff_id, n_tg_id)
