import telebot
import json
import os
import time
from datetime import datetime

# ===== КОНФИГ (ВСТАВЬ СВОИ ДАННЫЕ) =====
TOKEN = "8927013650:AAEDnVjrp6MJH6v5KyKJ10PTyq1uLO6Ywy4"
YOUR_ID = 8698370995  # ТВОЙ ID (тот, что получил от @userinfobot)
# ========================================

CHAT_FILE = "chats.json"
MESSAGE_FILE = "message.txt"

bot = telebot.TeleBot(TOKEN)

def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

def load_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "⚠️ Текст рассылки не задан"

def send_broadcast():
    # ==== ТЕСТОВОЕ СООБЩЕНИЕ ТЕБЕ (ЧТОБЫ ЗНАТЬ, ЧТО ЗАПУСТИЛОСЬ) ====
    try:
        bot.send_message(YOUR_ID, "🚀 Запущена автоматическая рассылка...")
    except:
        pass

    chat_ids = load_chats()
    if not chat_ids:
        bot.send_message(YOUR_ID, "❌ Нет чатов в chats.json. Добавь ID.")
        return

    text = load_message()
    if not text or text == "⚠️ Текст рассылки не задан":
        bot.send_message(YOUR_ID, "❌ Нет текста в message.txt")
        return

    sent = 0
    failed = 0
    for cid in list(chat_ids):
        try:
            bot.send_message(cid, text)
            time.sleep(0.1)
            sent += 1
        except Exception as e:
            failed += 1
            print(f"Ошибка для {cid}: {e}")

    report = (
        f"✅ **Рассылка завершена**\n"
        f"📨 Отправлено: {sent}\n"
        f"❌ Ошибок: {failed}\n"
        f"📋 Чатов: {len(chat_ids)}\n"
        f"🕒 {datetime.now().strftime('%H:%M')}"
    )
    bot.send_message(YOUR_ID, report)

if __name__ == "__main__":
    send_broadcast()
