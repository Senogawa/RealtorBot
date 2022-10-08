from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from loader import bot_meta

bot = Bot(bot_meta.token)
dp = Dispatcher(bot, storage = MemoryStorage())




async def bot_start_pooling():
    try:
        await dp.start_polling()
    finally:
        dp.storage.close()




if __name__ == "__main__":
    asyncio.run(bot_start_pooling())