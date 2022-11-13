from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from config_module import set_config_parameter
from config_module import create_config_data_message

async def delete_admin(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    admins_list = config_data.get("admins").split(", ")

    if str(message.from_id) != config_data.get("root"):
        await message.answer("У вас более нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board, parse_mode = "HTML")
        await BotStates.form_type_state.set()
        return
    
    elif message.text == "Назад":
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    elif message.text.isdigit() and message.text in admins_list:
        admins_list.remove(message.text)
        admins_list = ",".join(admins_list)
        print(admins_list)
        set_config_parameter("TELEGRAM", "admins", admins_list)
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return



    await message.answer("id администратора должно состоять только из цифр")
    return