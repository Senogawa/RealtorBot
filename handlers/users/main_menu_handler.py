from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates


async def start(message: types.Message, state: FSMContext):
    bot_message = """Это первичная версия бота, не содержащая админ меню, оплаты и базы данных.
Данная версия демонстрирует взаимодействие клиента с сервисом,
настройку параметров поиска и получения информации об объявлениях.

Сейчас вы будете переброшены в главное меню."""
    await message.answer(bot_message)
    await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
    await state.set_data({
            "form_type":list(),
            "form_type_names":list()

    })
    await BotStates.form_type_state.set()



def register_all_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands = "start")