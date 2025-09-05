import telebot
from telebot import types

TOKEN = "8349223686:AAFBn4IgVS6M1n_0LYQjdZDl-dgF88ppm0E"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# user_id -> "tg" | "ru"
user_lang = {}

CATEGORIES = {"learning", "events", "center", "students"}

# Словарь с текстами для каждого подпункта
DATA = {
    "ru": {
        "learning_1": "<b>Расписание:</b>\nНаши занятия проходят по будням с 10:00 до 18:00. Возможны индивидуальные занятия по договорённости.",
        "learning_2": "<b>Цена:</b>\nМесячный абонемент стоит 500 сомони. Первое пробное занятие бесплатно.",
        "learning_3": "<b>Как записаться:</b>\nДля записи приходите к нам в офис с паспортом или звоните по номеру: +992 (ххх) ххх-ххх.",
        "learning_4": "<b>Документы:</b>\nДля оформления необходим паспорт и 2 фотографии 3x4.",
        "events_1": "<b>Культурные мероприятия:</b>\nМы регулярно проводим вечера поэзии и кинопоказы, посвящённые культуре Таджикистана.",
        "events_2": "<b>Календарь событий:</b>\nСледите за нашими анонсами в Telegram-канале!",
        "events_3": "<b>Конкурсы/Олимпиады:</b>\nЕжегодно мы проводим олимпиаду по русскому языку среди наших студентов.",
        "center_1": "<b>Адрес + карта:</b>\nНаш адрес: г. Душанбе, ул. Рудаки, 122.",
        "center_2": "<b>Контакты:</b>\nТелефон: +992 (999) 888-777\nE-mail: info@center.tj",
        "center_3": "<b>Часы работы:</b>\nПн-Пт: 09:00 - 19:00\nСб: 10:00 - 15:00\nВс: Выходной",
        "center_4": "<b>Преподаватели:</b>\nНаши преподаватели — это опытные носители языка с многолетним стажем.",
        "students_1": "<b>Домашние задания:</b>\nДомашние задания публикуются в отдельном чате для студентов.",
        "students_2": "<b>Аудио/Видео:</b>\nВесь учебный материал доступен на нашей платформе.",
        "students_3": "<b>Система уровней:</b>\nУ нас есть 6 уровней обучения, от A1 до C2.",
        "students_4": "<b>Чат с преподавателями:</b>\nВы можете задать вопрос преподавателю в нашем чате с 9:00 до 18:00.",
    },
    "tg": {
        "learning_1": "<b>Нақшаи дарсҳо:</b>\nДарсҳои мо ҳар рӯзҳои корӣ аз соати 10:00 то 18:00 баргузор мешаванд. Дарсҳои инфиродӣ низ имконпазиранд.",
        "learning_2": "<b>Нарх:</b>\nНархи абонементи моҳона 500 сомонӣ аст. Дарси аввали таҷрибавӣ ройгон аст.",
        "learning_3": "<b>Чӣ тавр сабти ном шавем:</b>\nБарои сабти ном бо шиноснома ба идораи мо муроҷиат кунед ё ба рақами +992 (ххх) ххх-ххх занг занед.",
        "learning_4": "<b>Ҳуҷҷатҳо:</b>\nБарои сабти ном шиноснома ва 2 акси 3х4 лозим аст.",
        "events_1": "<b>Фаъолиятҳои фарҳангӣ:</b>\nМо мунтазам шомҳои шеъру филмбардории фарҳанги тоҷикиро баргузор мекунем.",
        "events_2": "<b>Тақвими рӯйдодҳо:</b>\nХабарҳои моро дар канали Telegram пайгирӣ кунед!",
        "events_3": "<b>Озмунҳо/Олимпиадаҳо:</b>\nМо ҳар сол дар байни донишҷӯён олимпиадаи забони русиро баргузор менамоем.",
        "center_1": "<b>Суроға + харита:</b>\nСуроғаи мо: ш. Душанбе, кӯчаи Рӯдакӣ, 122.",
        "center_2": "<b>Алоқа:</b>\nТелефон: +992 (999) 888-777\nE-mail: info@center.tj",
        "center_3": "<b>Соатҳои корӣ:</b>\nДш-Ҷм: 09:00 - 19:00\nШн: 10:00 - 15:00\nЯкш: Рӯзи истироҳатӣ",
        "center_4": "<b>Омӯзгорон:</b>\nОмӯзгорони мо мутахассисони ботаҷриба ва дорандагони забон мебошанд.",
        "students_1": "<b>Вазифаҳои хонагӣ:</b>\nВазифаҳои хонагӣ дар чати махсуси донишҷӯён нашр мешаванд.",
        "students_2": "<b>Аудио/Видео:</b>\nҲамаи маводи таълимӣ дар платформаи мо дастрас аст.",
        "students_3": "<b>Системаи сатҳҳо:</b>\nМо 6 сатҳи омӯзиш дорем, аз A1 то C2.",
        "students_4": "<b>Чат бо омӯзгорон:</b>\nШумо метавонед саволҳои худро ба омӯзгор дар чати мо аз соати 9:00 то 18:00 диҳед.",
    },
}


# ====== /start ======
@bot.message_handler(commands=["start"])
def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Используем невидимый символ для создания отступа.
    kb.add(
        types.InlineKeyboardButton("🇹🇯 Таджикский", callback_data="lang_tg"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
    )
    bot.send_message(message.chat.id, "Выберите язык:", reply_markup=kb)


# ====== Выбор языка ======
@bot.callback_query_handler(func=lambda c: c.data in {"lang_tg", "lang_ru"})
def on_lang_pick(call: types.CallbackQuery):
    uid = call.from_user.id
    user_lang[uid] = "tg" if call.data == "lang_tg" else "ru"
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_main_menu(call.message.chat.id, user_lang[uid])
    bot.answer_callback_query(call.id)


# ====== Главное меню ======
def send_main_menu(chat_id, lang):
    kb = types.InlineKeyboardMarkup(row_width=1)
    if lang == "tg":
        kb.add(
            types.InlineKeyboardButton("📚 Дарсҳо" + " " * 10, callback_data="learning"),
            types.InlineKeyboardButton("🎉 Фаъолиятҳо" + " " * 10, callback_data="events"),
            types.InlineKeyboardButton("📍 Марказ" + " " * 10, callback_data="center"),
            types.InlineKeyboardButton("📑 Барои донишҷӯён" + " " * 10, callback_data="students"),
        )
        text = "📩 Шумо чӣ мехостед донед?"
    else:
        kb.add(
            types.InlineKeyboardButton("📚 Обучение" + " " * 10, callback_data="learning"),
            types.InlineKeyboardButton("🎉 Мероприятия" + " " * 10, callback_data="events"),
            types.InlineKeyboardButton("📍 Центр" + " " * 10, callback_data="center"),
            types.InlineKeyboardButton("📑 Для студентов" + " " * 10, callback_data="students"),
        )
        text = "📩 Что вы хотели узнать?"
    bot.send_message(chat_id, text, reply_markup=kb)


# ====== Подменю ======
def show_submenu(chat_id, lang, category):
    kb = types.InlineKeyboardMarkup(row_width=1)

    items = {
        "learning": ["🕐 Расписание", "💵 Цена", "📝 Как записаться", "📄 Документы"],
        "events": ["🎉 Культурные мероприятия", "📅 Календарь событий", "🎤 Конкурсы/Олимпиады"],
        "center": ["📍 Адрес + карта", "☎️ Контакты", "⏰ Часы работы", "👩‍🏫 Преподаватели"],
        "students": ["📑 Домашние задания", "🎧 Аудио/Видео", "🏆 Система уровней", "💬 Чат с преподавателями"],
    }

    # Максимальная длина текста для выравнивания
    max_len = max(len(text) for text in items[category])

    for i, text in enumerate(items[category], 1):
        # Добавляем пробелы, чтобы выровнять текст.
        # Вычисление количества пробелов для каждой кнопки.
        spaces_count = max_len - len(text)
        kb.add(types.InlineKeyboardButton(text + " " * spaces_count, callback_data=f"{category}_{i}"))

    # назад в главное
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))

    titles = {
        "learning": "📚 Обучение:" if lang == "ru" else "📚 Дарсҳо:",
        "events": "🎉 Мероприятия:" if lang == "ru" else "🎉 Фаъолиятҳо:",
        "center": "📍 Центр:" if lang == "ru" else "📍 Марказ:",
        "students": "📑 Для студентов:" if lang == "ru" else "📑 Барои донишҷӯён:",
    }

    bot.send_message(chat_id, titles[category], reply_markup=kb)


# ====== Выбор категории (главное → подменю) ======
@bot.callback_query_handler(func=lambda c: c.data in CATEGORIES)
def on_category_pick(call: types.CallbackQuery):
    uid = call.from_user.id
    lang = user_lang.get(uid, "ru")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_submenu(call.message.chat.id, lang, call.data)
    bot.answer_callback_query(call.id)


# ====== Подпункты (подменю → детальная инфо) ======
# Строгий фильтр: <category>_<number>, например "learning_1"
@bot.callback_query_handler(
    func=lambda c: (
            "_" in c.data
            and c.data.split("_", 1)[0] in CATEGORIES
            and c.data.split("_", 1)[1].isdigit()
    )
)
def on_subitem_pick(call: types.CallbackQuery):
    category = call.data.split("_", 1)[0]
    subitem_key = call.data
    lang = user_lang.get(call.from_user.id, "ru")  # Получаем язык пользователя

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=f"{category}_back"))

    # Получаем текст из словаря DATA. Если текст не найден, отправляем заглушку.
    text = DATA[lang].get(subitem_key, "ℹ️ Информация по разделу скоро будет обновлена.")

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)


# ====== Назад к подменю (из подпункта) ======
@bot.callback_query_handler(
    func=lambda c: c.data.endswith("_back") and c.data.split("_", 1)[0] in CATEGORIES
)
def back_to_submenu(call: types.CallbackQuery):
    uid = call.from_user.id
    lang = user_lang.get(uid, "ru")
    category = call.data.split("_", 1)[0]
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_submenu(call.message.chat.id, lang, category)
    bot.answer_callback_query(call.id)


# ====== Назад в главное (из подменю) ======
@bot.callback_query_handler(func=lambda c: c.data == "back_main")
def back_to_main(call: types.CallbackQuery):
    uid = call.from_user.id
    lang = user_lang.get(uid, "ru")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_main_menu(call.message.chat.id, lang)
    bot.answer_callback_query(call.id)


if __name__ == "__main__":
    bot.polling(none_stop=True)