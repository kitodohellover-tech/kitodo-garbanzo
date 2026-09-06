import telebot
import os

BOT_TOKEN = os.getenv("8934134955:AAHbLmbcQYt3sccFlDvEcJZJg3OFv0Yyneg")  # токен возьмём из настроек, не в коде

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот работает из облака. Напиши что-нибудь.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

print("Бот запущен")
bot.polling(none_stop=True)
