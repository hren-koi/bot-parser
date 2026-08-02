import telebot
import os
import json

# ===== ВСТАВЬ СВОИ ДАННЫЕ =====
TOKEN = "8927013650:AAEDnVjrp6MJH6v5KyKJ10PTyq1uLO6Ywy4"
MY_ID = 8698370995  # ← СЮДА ВСТАВЬ ЧИСЛО, КОТОРОЕ ДАЛ @userinfobot
# ===============================

bot = telebot.TeleBot(TOKEN)

# ПРОСТО ОТПРАВЛЯЕМ СООБЩЕНИЕ — БЕЗ ВСЯКИХ ПРОВЕРОК
try:
    bot.send_message(MY_ID, "✅ БОТ РАБОТАЕТ! Это тестовое сообщение.")
    print("✅ Сообщение отправлено успешно!")
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
