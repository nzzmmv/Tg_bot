from telebot import types
from data import CATEGORIES, DATA
from keyboards import send_main_menu, show_submenu

user_lang = {}

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message: types.Message):
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton("🇹🇯 Таджикский", callback_data="lang_tg"),
            types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        )
        bot.send_message(message.chat.id, "Выберите язык:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data in {"lang_tg", "lang_ru"})
    def on_lang_pick(call: types.CallbackQuery):
        uid = call.from_user.id
        user_lang[uid] = "tg" if call.data == "lang_tg" else "ru"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_main_menu(call.message.chat.id, user_lang[uid], bot)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data in CATEGORIES)
    def on_category_pick(call: types.CallbackQuery):
        uid = call.from_user.id
        lang = user_lang.get(uid, "ru")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_submenu(call.message.chat.id, lang, call.data, bot)
        bot.answer_callback_query(call.id)

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
        lang = user_lang.get(call.from_user.id, "ru")

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=f"{category}_back"))

        text = DATA[lang].get(subitem_key, "ℹ️ Информация по разделу скоро будет обновлена.")

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(
        func=lambda c: c.data.endswith("_back") and c.data.split("_", 1)[0] in CATEGORIES
    )
    def back_to_submenu(call: types.CallbackQuery):
        uid = call.from_user.id
        lang = user_lang.get(uid, "ru")
        category = call.data.split("_", 1)[0]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_submenu(call.message.chat.id, lang, category, bot)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == "back_main")
    def back_to_main(call: types.CallbackQuery):
        uid = call.from_user.id
        lang = user_lang.get(uid, "ru")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_main_menu(call.message.chat.id, lang, bot)
        bot.answer_callback_query(call.id)
