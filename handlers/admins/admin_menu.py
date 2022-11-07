from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import get_config_data


async def admin_main_menu(message: types.Message, state: FSMContext):
    admins_list = get_config_data().get("admins").split(",")
    if str(message.from_id) not in admins_list:
        await message.answer("У вас более нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return
        
    if message.text == "Добавить администратора" and str(message.from_id) in admins_list:
        await message.answer("Введите id администратора\n\nПример: 10856723", reply_markup = Boards.back_button_board)
        await BotStates.add_admin_state.set()
        return

    elif message.text == "Изменить количество форм для поиска" and str(message.from_id) in admins_list:
        await message.answer("Введите количество форм для поиска\n\nПример: 15", reply_markup = Boards.back_button_board)
        await BotStates.change_forms_quantity_state.set()
        return

    elif message.text == "Изменить количество пробных поисков" and str(message.from_id) in admins_list:
        await message.answer("Введите количество пробных поисков\n\nПример: 3", reply_markup = Boards.back_button_board)
        await BotStates.change_trials_finds_quantity_state.set()
        return

    elif message.text == "Изменить количество пробных форм для поиска" and str(message.from_id) in admins_list:
        await message.answer("Введите количество пробных форм для поиска\n\nПример: 15", reply_markup = Boards.back_button_board)
        await BotStates.change_trials_finds_form_quantity_state.set()
        return

    elif message.text == "Назад" and str(message.from_id) in admins_list:
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board_admin)
        await BotStates.form_type_state.set()
        return

    
def register_all_admin_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_main_menu, state = BotStates.admin_menu_state)