from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates




def register_all_admin_menu_handlers(dp: Dispatcher):
    ...