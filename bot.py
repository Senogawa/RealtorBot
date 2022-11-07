from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from handlers.users.main_menu_handler import register_all_main_menu_handlers
from handlers.users.collect_info_about_form import register_all_collecting_info_handlers
from handlers.users.accept_form_data import register_all_accept_form_data_handlers
from  handlers.users.sell_or_rent_handler import register_all_sell_or_rent_handlers
from handlers.users.price_from_to_handler import register_all_price_from_to_handler
from handlers.users.streets_or_stations_handler import register_all_streets_or_stations_handlers
from handlers.users.confirmation_handler import register_all_confirmation_handlers
from handlers.admins.admin_menu import register_all_admin_menu_handlers

from loader import bot_meta

bot = Bot(bot_meta.token)
dp = Dispatcher(bot, storage = MemoryStorage())


register_all_main_menu_handlers(dp)
register_all_collecting_info_handlers(dp)
register_all_accept_form_data_handlers(dp)
register_all_sell_or_rent_handlers(dp)
register_all_price_from_to_handler(dp)
register_all_streets_or_stations_handlers(dp)
register_all_confirmation_handlers(dp)
register_all_admin_menu_handlers(dp)

async def bot_start_pooling():
    try:
        await dp.start_polling()
    finally:
        dp.storage.close()




if __name__ == "__main__":
    asyncio.run(bot_start_pooling())