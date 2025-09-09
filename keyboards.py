from telebot import types # type: ignore

MAIN_MENU_TEXT = {
    "ru": {
        "text": "📩 Что вы хотели узнать?",
        "buttons": {
            "learning": "📚 Обучение",
            "events": "🎉 Мероприятия",
            "center": "📍 Центр",
            "students": "📑 Для студентов",
            "gemini_chat": "🤖 Задать вопрос AI",
        }
    },
    "tg": {
        "text": "📩 Шумо чӣ мехостед донед?",
        "buttons": {
            "learning": "📚 Дарсҳо",
            "events": "🎉 Фаъолиятҳо",
            "center": "📍 Марказ",
            "students": "📑 Барои донишҷӯён",
            "gemini_chat": "🤖 Савол додан ба AI",
        }
    }
}

SUBMENU_ITEMS = {
    "learning": ["🕐 Расписание", "💵 Цена", "📝 Как записаться", "📄 Документы"],
    "events": ["🎉 Культурные мероприятия", "📅 Календарь событий"],
    "center": ["📍 Адрес", "☎️ Контакты", "⏰ Часы работы",],
    "students": ["📑 Домашние задания", "🏆 Система обучения"],
}

SUBMENU_TITLES = {
    "ru": {
        "learning": "📚 Обучение:",
        "events": "🎉 Мероприятия:",
        "center": "📍 Центр:",
        "students": "📑 Для студентов:",
    },
    "tg": {
        "learning": "📚 Дарсҳо:",
        "events": "🎉 Фаъолиятҳо:",
        "center": "📍 Марказ:",
        "students": "📑 Барои донишҷӯён:",
    }
}

def send_main_menu(chat_id, lang, bot):
    kb = types.InlineKeyboardMarkup(row_width=1)
    menu_data = MAIN_MENU_TEXT[lang]
    buttons = [
        types.InlineKeyboardButton(text, callback_data=callback_data)
        for callback_data, text in menu_data["buttons"].items()
    ]
    kb.add(*buttons)
    bot.send_message(chat_id, menu_data["text"], reply_markup=kb)

def show_submenu(chat_id, lang, category, bot):
    kb = types.InlineKeyboardMarkup(row_width=1)
    items = SUBMENU_ITEMS[category]
    for i, text in enumerate(items, 1):
        kb.add(types.InlineKeyboardButton(text, callback_data=f"{category}_{i}"))

    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))
    title = SUBMENU_TITLES[lang][category]
    bot.send_message(chat_id, title, reply_markup=kb)
