import telebot
import json
import os
import time
from datetime import datetime

# ==========================================
#   КОНФИГ (ЗАМЕНИ НА СВОЁ)
# ==========================================
TOKEN = "8927013650:AAEDnVjrp6MJH6v5KyKJ10PTyq1uLO6Ywy4"
YOUR_ID = 8698370995  # ТВОЙ TELEGRAM ID
# ==========================================

CHAT_FILE = "chats.json"
MESSAGE_FILE = "message.txt"
LOG_FILE = "log.txt"  # Файл для логов (опционально)

bot = telebot.TeleBot(TOKEN)

# ===== ЗАГРУЗКА ЧАТОВ =====
def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

# ===== ЗАГРУЗКА ТЕКСТА РАССЫЛКИ =====
def load_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "⚠️ Текст рассылки не задан"

# ===== ЗАПИСЬ ЛОГА (ДЛЯ ОТСЛЕЖИВАНИЯ) =====
def write_log(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

# ===== ОТПРАВКА РАССЫЛКИ =====
def send_broadcast():
    chat_ids = load_chats()
    if not chat_ids:
        print("❌ Нет чатов")
        write_log("Нет чатов для рассылки")
        return

    text = load_message()
    if not text:
        print("❌ Текст пуст")
        write_log("Текст рассылки пуст")
        return

    sent = 0
    failed = 0

    for cid in list(chat_ids):
        try:
            bot.send_message(cid, text)
            time.sleep(0.1)  # чуть меньше задержка для скорости
            sent += 1
        except Exception as e:
            failed += 1
            write_log(f"Ошибка для {cid}: {str(e)[:50]}")

    # ===== ОТЧЁТ ТЕБЕ =====
    report = (
        f"✅ **Рассылка (5 мин)**\n"
        f"📨 Отправлено: {sent}\n"
        f"❌ Ошибок: {failed}\n"
        f"📋 Чатов: {len(chat_ids)}\n"
        f"🕒 {datetime.now().strftime('%H:%M')}"
    )
    try:
        bot.send_message(YOUR_ID, report)
    except:
        pass

    write_log(f"Отправлено: {sent}, ошибок: {failed}")

# ===== ТОЧКА ВХОДА =====
if __name__ == "__main__":
    print("🚀 Запуск рассылки (5 мин)...")
    send_broadcast()
    print("✅ Готово")
