from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import get_config_data



async def start(message: types.Message, state: FSMContext):
    bot_message = """Это первичная версия бота, не содержащая админ меню, оплаты и базы данных.
Данная версия демонстрирует взаимодействие клиента с сервисом,
настройку параметров поиска и получения информации об объявлениях.

Сейчас вы будете переброшены в главное меню."""

    admins_list = get_config_data().get("admins").split(",")
    form_type_board = Boards.form_type_board
    if str(message.from_id) in admins_list:
        form_type_board = Boards.form_type_board_admin

    await message.answer(bot_message)
    await message.answer("Выберите тип объявления", reply_markup = form_type_board)
    await state.set_data({
            "form_type":list(),
            "form_type_names":list()

    })
    del form_type_board
    await BotStates.form_type_state.set()



def register_all_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands = "start")