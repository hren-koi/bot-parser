import telebot
import json
import os
import time
import requests
from datetime import datetime

# === ВСТАВЬ СВОИ ДАННЫЕ СЮДА ===
TOKEN = "8927013650:AAEDnVjrp6MJH6v5KyKJ10PTyq1uLO6Ywy4"  # Твой токен от BotFather
YOUR_ID = 8698370995  # Твой Telegram ID (число, без кавычек)
PROXY = None  # Если используешь прокси, напиши "http://user:pass@ip:port", иначе None
# ================================

# === ИНИЦИАЛИЗАЦИЯ ===
bot = telebot.TeleBot(TOKEN)
if PROXY:
    telebot.apihelper.proxy = {'https': PROXY}

CHAT_FILE = "chats.json"

# === ЗАГРУЗКА СПИСКА ЧАТОВ ===
def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

def save_chats(chats):
    with open(CHAT_FILE, "w") as f:
        json.dump(list(chats), f)

chat_ids = load_chats()

# === ФУНКЦИЯ РАССЫЛКИ ===
def send_broadcast(text, photo_url=None, file_url=None):
    success = 0
    failed = 0
    for cid in list(chat_ids):
        try:
            if photo_url:
                bot.send_photo(cid, photo_url, caption=text)
            elif file_url:
                bot.send_document(cid, file_url, caption=text)
            else:
                bot.send_message(cid, text)
            time.sleep(0.15)
            success += 1
        except Exception as e:
            error_text = str(e)
            if "bot was blocked" in error_text or "chat not found" in error_text or "user is deactivated" in error_text:
                chat_ids.discard(cid)
                failed += 1
            else:
                print(f"Ошибка для {cid}: {error_text[:50]}")
            continue
    save_chats(chat_ids)
    return success, failed

# === ПОЛУЧЕНИЕ ПОСЛЕДНЕЙ КОМАНДЫ ===
def get_last_command():
    try:
        updates = bot.get_updates(offset=-1, limit=10)
        for update in reversed(updates):
            msg = update.message
            if msg and msg.from_user.id == YOUR_ID and msg.text:
                if msg.text.startswith('/broadcast'):
                    parts = msg.text.replace('/broadcast', '', 1).strip().split('|')
                    text = parts[0].strip()
                    photo = parts[1].strip() if len(parts) > 1 and 'http' in parts[1] else None
                    file = parts[2].strip() if len(parts) > 2 and 'http' in parts[2] else None
                    return text, photo, file, msg.message_id
                elif msg.text.startswith('/addchat'):
                    try:
                        new_id = int(msg.text.replace('/addchat', '').strip())
                        chat_ids.add(new_id)
                        save_chats(chat_ids)
                        bot.send_message(YOUR_ID, f"✅ Чат {new_id} добавлен. Всего: {len(chat_ids)}")
                    except:
                        bot.send_message(YOUR_ID, "❌ Неверный ID. Используй /addchat 123456789")
                elif msg.text.startswith('/stats'):
                    bot.send_message(YOUR_ID, f"📊 Всего чатов: {len(chat_ids)}")
    except Exception as e:
        print(f"Ошибка get_updates: {e}")
    return None, None, None, None

# === ОСНОВНОЙ ЗАПУСК ===
if __name__ == "__main__":
    text, photo, file, msg_id = get_last_command()
    if text:
        sent, failed = send_broadcast(text, photo, file)
        report = f"✅ Рассылка завершена\n📨 Отправлено: {sent}\n❌ Удалено неактивных: {failed}\n📋 Всего чатов: {len(chat_ids)}\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        bot.send_message(YOUR_ID, report)
    else:
        bot.send_message(YOUR_ID, f"⏳ Нет новых команд. Чатов в базе: {len(chat_ids)}")
