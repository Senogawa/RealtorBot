from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from config_module import set_config_parameter
from config_module import create_config_data_message

async def change_trials_finds_quantity(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    admins = config_data.get("admins").split(", ")
    admins.append(get_config_data().get("root"))
    admin_board = Boards.admin_board
    if str(message.from_id) == config_data.get("root"):
        admin_board = Boards.root_board

    if str(message.from_id) not in admins:
        await message.answer("У вас более нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board, parse_mode = "HTML")
        await BotStates.form_type_state.set()
        return
    
    elif message.text == "Назад":
        await message.answer(create_config_data_message()[1], reply_markup = admin_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    elif message.text.isdigit() and str(message.from_id) in admins:
        set_config_parameter("SMARTAGENT", "trials_finds_quantity", message.text)
        await message.answer(create_config_data_message()[1], reply_markup = admin_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return



    await message.answer("Количество пробных поисков должно состоять только из цифр")
    return