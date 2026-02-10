import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.config import BOT_TOKEN


def main_menu_keyboard() -> ReplyKeyboardBuilder:
    """
    Временное меню без WebApp-кнопки.
    Позже сюда вернём кнопку с Mini App, когда появится HTTPS-URL.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(
        text="(пока без Mini App)"  # обычная кнопка
    )
    kb.adjust(1)
    return kb


async def on_startup(bot: Bot):
    print("Бот запущен")


async def main():
    # Создаём бота и диспетчер внутри main (важно для event loop)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(F.text == "/start")
    async def cmd_start(message: Message):
        await message.answer(
            "Привет! Бот живёт. Mini App подключим, когда появится HTTPS-URL (Amvera или ngrok).",
            reply_markup=main_menu_keyboard().as_markup(resize_keyboard=True)
        )

    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
