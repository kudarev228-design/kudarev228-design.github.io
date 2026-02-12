import asyncio
import json
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp
from aiogram.enums import MenuButtonType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "ВАШ_ТОКЕН_БОТА"
WEBAPP_URL = "https://ваш-логин.github.io/репозиторий/"  # URL мини-приложения

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---- База данных (SQLite) ----
def init_db():
    conn = sqlite3.connect('vpn_users.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            tariff TEXT,
            key TEXT,
            expires TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            tariff TEXT,
            used INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# ---- Команда /start ----
@dp.message(Command('start'))
async def start_cmd(message: Message):
    # Устанавливаем кнопку меню с Web App (будет видна всегда)
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            type=MenuButtonType.WEB_APP,
            text="🇷🇺 Купить VPN",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    # Приветственное сообщение в стиле СССР
    await message.answer(
        "☭ **ДОБРО ПОЖАЛОВАТЬ В RUSSIAN BOSS VPN!** ☭\n\n"
        "Товарищ, мы предлагаем надёжное соединение вне зоны действия империалистической цензуры.\n"
        "Нажми на кнопку внизу экрана, чтобы выбрать тариф и получить ключ.\n\n"
        "С нами — свобода, равенство и скорость!",
        parse_mode="Markdown"
    )

# ---- Получение данных из Web App ----
@dp.message(web_app_data=types.WebAppData)
async def web_app_handler(message: Message):
    data = json.loads(message.web_app_data.data)
    if data.get('action') == 'buy':
        tariff = data.get('tariff')
        # Здесь логика: проверить оплату, выдать ключ
        # Для примера – выдаём тестовый ключ
        vpn_key = f"СССР-{tariff}-{message.from_user.id}"
        await message.answer(
            f"🎖 **ТАРИФ «{tariff.upper()}» АКТИВИРОВАН!**\n\n"
            f"Ваш ключ доступа:\n`{vpn_key}`\n\n"
            f"Инструкция по настройке: /help",
            parse_mode="Markdown"
        )
        # Сохраняем в БД
        conn = sqlite3.connect('vpn_users.db')
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO users (user_id, username, tariff, key) VALUES (?, ?, ?, ?)",
            (message.from_user.id, message.from_user.username, tariff, vpn_key)
        )
        conn.commit()
        conn.close()

# ---- Команда помощи ----
@dp.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(
        "📡 **НАСТРОЙКА ПОДКЛЮЧЕНИЯ**\n\n"
        "1. Скопируйте ключ доступа.\n"
        "2. Скачайте приложение Outline / WireGuard.\n"
        "3. Импортируйте ключ.\n"
        "4. Нажмите «Подключиться».\n\n"
        "Если возникли проблемы — пишите @support_username",
        parse_mode="Markdown"
    )

# ---- Запуск ----
async def main():
    init_db()
    print("Бот RussianBossVPN запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
