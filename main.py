import telebot # type: ignore
from config import TOKEN
from handlers import register_handlers

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
    register_handlers(bot)
    bot.polling(none_stop=True)
