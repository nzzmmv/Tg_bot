import telebot # type: ignore
from telebot import types # type: ignore
from config import TOKEN
from handlers import register_handlers

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

    # Define bot commands for the menu
    commands = [
        types.BotCommand("menu", "Показать главное меню"),
        types.BotCommand("clear_chat", "Очистить и завершить чат с AI"),
        types.BotCommand("cancel", "Выйти из чата с AI"),
        types.BotCommand("refresh", "Перезапустить бота для пользователя"),
    ]
    bot.set_my_commands(commands)

    register_handlers(bot)
    print("Bot started...")
    bot.polling(none_stop=True)
    print("Bot stopped.")
