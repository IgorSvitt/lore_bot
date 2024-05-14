import re

lang_dict = {
    'ru': {
        'chosen_language': "Выбран русский язык",
        'like': "Нравится 🟢",
        'dislike': "🔴 Не нравится",
        'find_ff': "Перейти к поиску работ🎀",
        'finder_greeting': "FanFinder это как Тиндер только для фанфиков 💥💥💥. Наш алгоритм подберет работу, "
                           "которая подходит именно тебе! 💜\n",
        'like_message': "Помогите алгоритму стать лучше! ❤️\n "
                        "Какие теги из тегов ниже ✨заинтересовали✨ Вас в данной работе?🤔🌞",
        'dislike_message': "Помогите алгоритму стать лучше! ❤️\n "
                           "Какие теги из тегов ниже 🚫не заинтересовали🚫 Вас в данной работе?🤔🌞",
        'all': "Все вышеперечисленное💯",
        'nothing': "Ничего из вышеперечисленного🚫",
        'skip': "Пропустить⏩",
        'fandoms_message': "Выберите один или несколько фандомов:\n"
                           "Их описание можно посмотреть с помощью команды /help",
        'tags_message': "Выберите один или несколько тегов: \n"
                        "Их описание можно посмотреть с помощью команды /help",
        'pairings_fandoms_message': "Ниже представлены каждый из выбранных Вами фандомов.\n"
                                    "Нажмите на название фандома, чтобы выбрать необходимые пейринги \n"
                                    "Их описание можно посмотреть с помощью команды /help",
        'pairings_common_message': "Вы не выбрали ни одного фандома, поэтому предлагаем вам выбрать интересующий тип "
                                   "отношений \n"
                                   "Их описание можно посмотреть с помощью команды /help",
        'pairings_message': "Выберите один или несколько пейрингов: \n",
        'cleared': "Список очищен",
        'clear': "Очистить мой список🗑",
        'choose_tag': "Настроить теги для поиска#️⃣",
        'choose_fandom': "Выбрать фандом🕸️",
        'activity': "Выберите действие: \n",
        'form': "Настроить мои предпочтения❤️",
        'finder': "Перейти к поиску фанфиков🔍",
        'favorites': "Моя коллекция📚",
        'back': "Назад◀️",
        'info': "Узнать больше о LORE ❓",
        'choose_pairings': "Выбрать пейринги 💑👩‍❤️‍💋‍👩👨‍❤️‍👨"
    },
    'en': {
        'chosen_language': "English language selected",
        'like': "Like 🟢",
        'dislike': "🔴Dislike",
        'find_ff': "Go to fanfic search🎀",
        'finder_greeting': "FanFinder is like a fanfiction-only Tinder. 💥💥💥 \n Our algorithm will select the ff "
                           " that is right for you! 💜\n",
        'like_message': "Help the algorithm become better! ❤️\n "
                        "Which tags from the tags below ✨are you interested✨ in this work?🤔🌞",
        'dislike_message': "Help the algorithm become better! ❤️\n "
                           "Which tags from the tags below you 🚫are not interested🚫in this work?🤔🌞",
        'all': "All of the above💯",
        'nothing': "None of the above🚫",
        'skip': "Skip⏩",
        'fandoms_message': "Select one or more fandoms:\n"
                           "Their description can be viewed using the /help command",
        'tags_message': "Select one or more tags: \n"
                        "Their description can be viewed using the /help command",
        'pairings_fandoms_message': "Below are each of the selected fandoms.\n"
                                    "Click on the name of the fandom to select the necessary pairings \n"
                                    "Their description can be viewed using the command /help",
        'pairings_common_message': "You have not selected any fandom, so we suggest you choose the type of "
                                   "relationship \n"
                                   "Their description can be viewed using the command /help",
        'pairings_message': "Select one or more pairings: \n",
        'cleared': "The list is cleared",
        'clear': "Purify my list🗑",
        'choose_tag': "Customize search tags#️⃣",
        'choose_fandom': "Choose the fandom🕸️",
        'activity': "Select an action: \n",
        'form': "Set my preferences❤️",
        'finder': "Go to search fanfiction🔍",
        'favorites': "My collection📚",
        'back': "Back◀️",
        'info': "to Learn more about the LORE ❓",
        'choose_pairings': "Choose pairings 💑👩❤️💋👩👨❤️👨"
    }
}


async def process_comas(message):
    list_of_phrases = message.split(',')
    return list_of_phrases


async def process_tags(message):
    splited_categories = message.split(";")
    list_categories_tags = []
    for category_pairing in splited_categories:
        parted = category_pairing.split(":")
        category = parted[0].strip()
        narrow_tags = await process_comas(parted[1].strip())
        list_categories_tags.append((category, narrow_tags))
    return list_categories_tags


async def process_post(message):
    pattern = r"«(.*?)» by (.*)"
    result = re.match(pattern, message)
    title = result.group(1)
    author = result.group(2)
    relationship = message.split('направление: ')[1].split('\n')[0]
    fandom = message.split('фандом: ')[1].split('\n')[0]
    tags = await process_tags(message.split('теги: ')[1].split('\n')[0])
    rating = message.split('рейтинг: ')[1].split('\n')[0]
    status = message.split('статус: ')[1].split('\n')[0]
    size = message.split('размер: ')[1].split('\n')[0]
    pairings = await process_comas(message.split('пейринг и персонажи: ')[1].split('\n')[0])
    description = message.split('описание: ')[1].split('\n')[0]
    url = message.split('ссылка: ')[1].split('\n')[0]
    return title, author, relationship, fandom, tags, rating, status, size, description, pairings, url
