import telebot # type: ignore
from telebot import types # type: ignore
import google.generativeai as genai
from data import CATEGORIES, DATA
from keyboards import send_main_menu, show_submenu
from config import GEMINI_API_KEY

user_lang = {}
user_state = {}

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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

    @bot.callback_query_handler(func=lambda c: c.data in CATEGORIES or c.data == "gemini_chat")
    def on_category_pick(call: types.CallbackQuery):
        uid = call.from_user.id
        lang = user_lang.get(uid, "ru")
        if call.data == "gemini_chat":
            user_state[uid] = "gemini_chat"
            bot.send_message(call.message.chat.id, "Вы вошли в режим чата с AI. Задайте свой вопрос. Для выхода введите /cancel")
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_submenu(call.message.chat.id, lang, call.data, bot)
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == "gemini_chat")
    def handle_gemini_chat(message: types.Message):
        try:
            lang = user_lang.get(message.from_user.id, "ru")
            
            # Prepare the knowledge base from DATA
            knowledge_base = ""
            if lang in DATA:
                for key, value in DATA[lang].items():
                    # Clean up the key to be more readable if needed, e.g., 'learning_1' -> 'learning 1'
                    # For now, we'll just use the value
                    knowledge_base += f"- {value}\n"

            system_prompt = (
                "You are an assistant for our educational center. "
                "You must only answer questions related to our center using the information provided below. "
                "If the user asks about any other topic, you must politely decline. "
                "If you don't know the answer from the provided information, say that you don't have that information."
                "\n--- Information Base ---\n"
                f"{knowledge_base}"
                "\n------------------------\n"
            )
            
            response = model.generate_content(system_prompt + "\n\nUser question: " + message.text)
            bot.send_message(message.chat.id, response.text)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")

    @bot.message_handler(commands=["cancel", "clear_chat"])
    def cancel_chat(message: types.Message):
        uid = message.from_user.id
        if user_state.get(uid) == "gemini_chat":
            user_state.pop(uid, None)
            lang = user_lang.get(uid, "ru")
            command = message.text.strip().lower()
            if command == '/clear_chat':
                bot.send_message(message.chat.id, "Чат очищен и вы вышли из режима чата с AI.")
            else:
                bot.send_message(message.chat.id, "Вы вышли из режима чата с AI.")
            send_main_menu(message.chat.id, lang, bot)

    @bot.message_handler(commands=['menu'])
    def menu(message: types.Message):
        lang = user_lang.get(message.from_user.id, "ru")
        send_main_menu(message.chat.id, lang, bot)

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