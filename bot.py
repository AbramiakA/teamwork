import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Токен бота (отримайте у @BotFather)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словник з тренажерами (номер: дані)
EQUIPMENT = {
    "1": {
        "name": "Біговий тренажер",
        "description": "Кардіо тренажер для розвитку витривалості та спалювання калорій. Підходить для розминки та основного тренування.",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Замініть на реальне відео
    },
    "2": {
        "name": "Жим лежачи",
        "description": "Базова вправа для розвитку грудних м'язів, передніх дельт та трицепсів. Важливо дотримуватися правильної техніки.",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Замініть на реальне відео
    },
    "3": {
        "name": "Присідання в Сміті",
        "description": "Безпечний варіант присідань для розвитку ніг та сідниць. Тренажер забезпечує стабільність руху.",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Замініть на реальне відео
    },
    "4": {
        "name": "Тяга верхнього блоку",
        "description": "Вправа для розвитку широчайших м'язів спини. Альтернатива підтягуванням для початківців.",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Замініть на реальне відео
    },
    "5": {
        "name": "Велотренажер",
        "description": "Кардіо тренажер для зміцнення ніг та покращення серцево-судинної системи. М'який вплив на суглоби.",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Замініть на реальне відео
    }
}

# Словник з тренерами
TRAINERS = {
    "Олександр Петренко": {
        "platform": "Telegram",
        "link": "https://t.me/trainer_alex",
        "message": "Привіт, хочу займатися з вами. Коли у вас є вільне місце цього тижня?"
    },
    "Марія Іваненко": {
        "platform": "Instagram", 
        "link": "https://instagram.com/maria_trainer",
        "message": "Привіт, хочу займатися з вами. Коли у вас є вільне місце цього тижня?"
    },
    "Дмитро Коваленко": {
        "platform": "WhatsApp",
        "link": "https://wa.me/380501234567",
        "message": "Привіт, хочу займатися з вами. Коли у вас є вільне місце цього тижня?"
    },
    "Анна Сидоренко": {
        "platform": "Telegram",
        "link": "https://t.me/anna_fitness",
        "message": "Привіт, хочу займатися з вами. Коли у вас є вільне місце цього тижня?"
    }
}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Обробка команди /start"""
    welcome_text = (
        "🏋️‍♂️ Вітаємо в нашому спортивному залі!\n\n"
        "Цей бот допоможе вам:\n"
        "• Правильно виконувати вправи на тренажерах\n"
        "• Зв'язатися з досвідченим тренером\n\n"
        "Введіть номер тренажера, щоб отримати інструкції 👇"
    )
    
    await message.answer(welcome_text)

@dp.message(F.text)
async def handle_equipment_number(message: types.Message):
    """Обробка введеного номера тренажера"""
    equipment_number = message.text.strip()
    
    if equipment_number in EQUIPMENT:
        equipment = EQUIPMENT[equipment_number]
        
        # Створюємо клавіатуру з кнопками
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="📹 Переглянути відео",
            url=equipment["video"]
        ))
        keyboard.add(InlineKeyboardButton(
            text="👨‍💼 Записатись до тренера",
            callback_data="book_trainer"
        ))
        keyboard.add(InlineKeyboardButton(
            text="🔙 Повернутися",
            callback_data="back_to_start"
        ))
        keyboard.adjust(1)  # По одній кнопці в рядку
        
        response_text = (
            f"🏋️‍♂️ **{equipment['name']}**\n\n"
            f"📝 {equipment['description']}\n\n"
            f"Натисніть кнопку нижче, щоб переглянути відео з правильною технікою виконання:"
        )
        
        await message.answer(
            response_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Тренажер з таким номером не знайдено.\n"
            "Будь ласка, введіть номер ще раз.\n\n"
            f"Доступні тренажери: {', '.join(EQUIPMENT.keys())}"
        )

@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    """Повернення до початку"""
    await callback.message.edit_text(
        "Введіть номер тренажера, щоб отримати інструкції 👇"
    )
    await callback.answer()

@dp.callback_query(F.data == "book_trainer")
async def show_trainers(callback: types.CallbackQuery):
    """Показати список тренерів"""
    keyboard = InlineKeyboardBuilder()
    
    for trainer_name, trainer_info in TRAINERS.items():
        keyboard.add(InlineKeyboardButton(
            text=f"{trainer_name} ({trainer_info['platform']})",
            callback_data=f"trainer_{trainer_name}"
        ))
    
    keyboard.add(InlineKeyboardButton(
        text="🔙 Повернутися",
        callback_data="back_to_start"
    ))
    keyboard.adjust(1)  # По одній кнопці в рядку
    
    await callback.message.edit_text(
        "👨‍💼 **Оберіть тренера:**\n\n"
        "Натисніть на ім'я тренера, щоб зв'язатися з ним:",
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("trainer_"))
async def contact_trainer(callback: types.CallbackQuery):
    """Контакт з тренером"""
    trainer_name = callback.data.replace("trainer_", "")
    
    if trainer_name in TRAINERS:
        trainer = TRAINERS[trainer_name]
        
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text=f"💬 Написати в {trainer['platform']}",
            url=trainer['link']
        ))
        keyboard.add(InlineKeyboardButton(
            text="🔙 Назад до тренерів",
            callback_data="book_trainer"
        ))
        keyboard.adjust(1)
        
        message_text = (
            f"👨‍💼 **{trainer_name}**\n\n"
            f"📱 Платформа: {trainer['platform']}\n\n"
            f"💬 **Готове повідомлення для копіювання:**\n"
            f"`{trainer['message']}`\n\n"
            f"Натисніть кнопку нижче, щоб перейти до {trainer['platform']} "
            f"та відправити повідомлення тренеру:"
        )
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="Markdown"
        )
    
    await callback.answer()

async def main():
    """Запуск бота"""
    print("🤖 Бот запускається...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
