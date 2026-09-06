import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Рабочая модель: если эта не сработает — замени на "llama-3.1-8b-instant"
MODEL = "llama-3.3-70b-versatile"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты полезный ассистент бота. Отвечай кратко, по делу, на русском языке."},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7
    }

    try:
        resp = requests.post(URL, json=payload, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        ai_reply = data["choices"]["message"]["content"]
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка AI: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
