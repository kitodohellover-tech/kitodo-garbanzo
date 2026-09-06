import telebot
import os
import threading
import time
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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

DAY_MAP = {
    "monday": "понедельник", "tuesday": "вторник", "wednesday": "среда",
    "thursday": "четверг", "friday": "пятница", "saturday": "суббота", "sunday": "воскресенье"
}

def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📅 Расписание на сегодня", callback_data="today"))
    markup.add(InlineKeyboardButton("📆 Расписание на завтра", callback_data="tomorrow"))
    markup.add(InlineKeyboardButton("📋 Всё расписание", callback_data="all"))
    markup.add(InlineKeyboardButton("💊 Напоминания", callback_data="pills_info"))
    return markup

def get_schedule_text(day_key):
    lines = SCHEDULE.get(day_key, ["Нет пар"])
    text = ""
    for line in lines:
        text += f"• {line}\n"
    return text

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
    text = "Привет! Я твой бот-помощник 🤖\nВыбери, что нужно:"
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "today":
        day_key = DAY_MAP.get(datetime.now().strftime("%A").lower(), "понедельник")
        text = f"📅 Расписание на сегодня ({day_key}):\n\n" + get_schedule_text(day_key)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())
    elif call.data == "tomorrow":
        day_key = DAY_MAP.get((datetime.now() + timedelta(days=1)).strftime("%A").lower(), "понедельник")
        text = f"📆 Расписание на завтра ({day_key}):\n\n" + get_schedule_text(day_key)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())
    elif call.data == "all":
        text = "📋 Полное расписание:\n\n"
        for day, pairs in SCHEDULE.items():
            text += f"📍 {day.title()}:\n"
            for line in pairs:
                text += f"  {line}\n"
            text += "\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())
    elif call.data == "pills_info":
        text = "💊 Напоминания о таблетках:\n\nУтро — 7:00\nВечер — 19:00\n\nНапоминания приходят автоматически."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message, f"Ты написал: {message.text}\n\nВыбери кнопку:", reply_markup=get_main_menu())

threading.Thread(target=remind_pills, daemon=True).start()
print("Бот запущен")
bot.polling(none_stop=True)
