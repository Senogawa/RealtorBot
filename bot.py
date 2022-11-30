from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from handlers.users.main_menu_handler import register_all_main_menu_handlers
from handlers.users.collect_info_about_form import register_all_collecting_info_handlers
from handlers.users.accept_form_data import register_all_accept_form_data_handlers
from handlers.users.sell_or_rent_handler import register_all_sell_or_rent_handlers
from handlers.users.price_from_to_handler import register_all_price_from_to_handler
from handlers.users.streets_or_stations_handler import register_all_streets_or_stations_handlers
from handlers.users.confirmation_handler import register_all_confirmation_handlers
from handlers.admins.admin_menu import register_all_admin_menu_handlers
from handlers.users.subscription_and_test_handler import register_all_subscription_and_test_handlers
from middlewares.payments.payments_handler import register_all_payments_handlers
from middlewares.scheduler.async_schedule_task import start_async_job
from threading import Thread

from loader import bot

loop = asyncio.new_event_loop()
dp = Dispatcher(bot, storage = MemoryStorage(), loop = loop)


register_all_main_menu_handlers(dp)
register_all_collecting_info_handlers(dp)
register_all_accept_form_data_handlers(dp)
register_all_sell_or_rent_handlers(dp)
register_all_price_from_to_handler(dp)
register_all_streets_or_stations_handlers(dp)
register_all_confirmation_handlers(dp)
register_all_admin_menu_handlers(dp)
register_all_subscription_and_test_handlers(dp)
register_all_payments_handlers(dp)

async def bot_start_pooling():
    try:
        Thread(target = start_async_job).start()
        await dp.start_polling()
    finally:
        dp.storage.close()




if __name__ == "__main__":
    asyncio.run(bot_start_pooling())