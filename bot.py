import telebot
import os
import threading
import time
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

YOUR_CHAT_ID = 8834374199

SCHEDULE = {
    "понедельник": [
        "1 пара (08:30–10:00): —",
        "2 пара (10:10–11:40): Разработка технических процессов — Ковалёв, каб. 104",
        "3 пара (13:00–14:30): Охрана труда и бережливое производство — Хитрова, каб. 107",
        "4 пара (14:40–16:10): Классный час",
        "5 пара (16:20–17:50): Организация — Стрельцова, каб. 206"
    ],
    "вторник": [
        "1 пара (08:30–10:00): Планирование организации работы / Эксплуатация подвижного состава — Стрельцова, каб. ОТТ-002",
        "2 пара (10:10–11:40): Эксплуатация железных дорог — Фалькин, каб. 111"
    ],
    "среда": [
        "1 пара (08:30–10:00): Разработка технических процессов — Ковалёв, каб. 104",
        "2 пара (10:10–11:40): Цифровая экономика — Баль, каб. 202",
        "3 пара (13:00–14:30): ТЭ и БЭД — Бударин, каб. 106 / ОХТ — Хитрова, каб. 107",
        "4 пара (14:40–16:10): Осмотрщик/ремонтник вагонов — Хитрова, каб. 107"
    ],
    "четверг": [
        "1 пара (08:30–10:00): Осмотрщик/ремонтник вагонов — Хитрова, каб. 107",
        "2 пара (10:10–11:40): Иностранный язык — Сагаева, каб. 109",
        "3 пара (13:00–14:30): Управление структурной деятельностью — Стрельцова",
        "4 пара (14:40–16:10): Планирование и работа структурных подразделений — Стрельцова"
    ],
    "пятница": [
        "1 пара (08:30–10:00): Транспортная безопасность — Шмыгла, каб. 003",
        "2 пара (10:10–11:40): Физкультура — Хамидуллин"
    ],
    "суббота": ["Выходной"],
    "воскресенье": ["Выходной"]
}

def remind_pills():
    last_sent = {"morning": None, "evening": None}
    while True:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        if now.hour == 7 and 0 <= now.minute < 2 and last_sent["morning"] != today:
            if YOUR_CHAT_ID:
                bot.send_message(YOUR_CHAT_ID, "💊 Пора принять утреннюю таблетку!")
            last_sent["morning"] = today
        if now.hour == 19 and 0 <= now.minute < 2 and last_sent["evening"] != today:
            if YOUR_CHAT_ID:
                bot.send_message(YOUR_CHAT_ID, "💊 Пора принять вечернюю таблетку!")
            last_sent["evening"] = today
        time.sleep(30)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой бот.\n/ucheba — расписание на сегодня\n/zavtra — на завтра\n/id — твой chat_id")

@bot.message_handler(commands=["ucheba"])
def show_schedule(message):
    day_map = {
        "monday": "понедельник", "tuesday": "вторник", "wednesday": "среда",
        "thursday": "четверг", "friday": "пятница", "saturday": "суббота", "sunday": "воскресенье"
    }
    current_day = day_map.get(datetime.now().strftime("%A").lower(), "понедельник")
    text = f"📅 Расписание на {current_day}:\n\n"
    for line in SCHEDULE.get(current_day, ["Нет пар"]):
        text += f"• {line}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=["zavtra"])
def show_tomorrow(message):
    day_map = {
        "monday": "понедельник", "tuesday": "вторник", "wednesday": "среда",
        "thursday": "четверг", "friday": "пятница", "saturday": "суббота", "sunday": "воскресенье"
    }
    tomorrow_day = day_map.get((datetime.now() + timedelta(days=1)).strftime("%A").lower(), "понедельник")
    text = f"📅 Расписание на завтра ({tomorrow_day}):\n\n"
    for line in SCHEDULE.get(tomorrow_day, ["Нет пар"]):
        text += f"• {line}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=["id"])
def show_id(message):
    bot.reply_to(message, f"Твой chat_id: {message.chat.id}\nСкопируй это число и вставь вместо None в коде.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

threading.Thread(target=remind_pills, daemon=True).start()
print("Бот запущен")
bot.polling(none_stop=True)
