import asyncio

from aiogram import Bot, Dispatcher, enums, types
from aiogram.client.default import DefaultBotProperties

from configs.settings import settings
from models.collection import Collection
from services.query import get_data
from storage.db import get_db


dp = Dispatcher()

db = get_db()


@dp.message()
async def get_employee_data(message: types.Message) -> None:
    data = await get_data(Collection.SAMPLE.value, message.text, db)

    await message.answer(data)


async def main() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML),
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
