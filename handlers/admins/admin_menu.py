from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from handlers.admins.add_admin_handler import add_admin
from handlers.admins.change_forms_quantity_handler import change_forms_quantity
from handlers.admins.change_trials_finds_quantity_handler import change_trials_finds_quantity
from handlers.admins.change_trials_finds_form_quantity_handler import change_trials_finds_form_quantity
from handlers.admins.delete_admin_handler import delete_admin
from handlers.admins.change_subs_handler import select_month, change_1_moth_price, change_2_moth_price, change_3_moth_price


async def admin_main_menu(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))
    if str(message.from_id) not in admins_list:
        await message.answer("У вас более нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return
        
    if message.text == "Добавить администратора" and str(message.from_id) == get_config_data().get("root"):
        await message.answer("Введите id администратора\n\nПример: 10856723", reply_markup = Boards.back_button_board)
        await BotStates.add_admin_state.set()
        return

    if message.text == "Удалить администратора" and str(message.from_id) == get_config_data().get("root"):
        admins_list = get_config_data().get("admins").split(", ")
        root_board_with_admins_list = types.ReplyKeyboardMarkup(resize_keyboard = True)
        for admin in admins_list:
            root_board_with_admins_list.add(admin)

        root_board_with_admins_list.add("Назад")
        await message.answer("Выберите id администратора \n\nПример: 10856723", reply_markup = root_board_with_admins_list)
        await BotStates.delete_admin_state.set()
        return
    
    elif message.text == "Удалить администратора" and str(message.from_id) != get_config_data().get("root"):
        await message.answer("У вас нет доступа к этой команде", reply_markup = Boards.admin_board)
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

    elif message.text == "Изменить стоимость подписок" and str(message.from_id) == get_config_data().get("root"):
        await message.answer("Выберите, какую стоимость изменить?", reply_markup = Boards.root_payments_board)
        await BotStates.change_subs_prices_state.set()
        return

    elif message.text == "Изменить стоимость подписок" and str(message.from_id) != get_config_data().get("root"):
        await message.answer("У вас нет доступа к этой команде", reply_markup = Boards.admin_board)
        return

    elif message.text == "Назад" and str(message.from_id) in admins_list:
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board_admin)
        await BotStates.form_type_state.set()
        return

    
def register_all_admin_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_main_menu, state = BotStates.admin_menu_state)
    dp.register_message_handler(add_admin, state = BotStates.add_admin_state)
    dp.register_message_handler(change_forms_quantity, state = BotStates.change_forms_quantity_state)
    dp.register_message_handler(change_trials_finds_quantity, state = BotStates.change_trials_finds_quantity_state)
    dp.register_message_handler(change_trials_finds_form_quantity, state = BotStates.change_trials_finds_form_quantity_state)
    dp.register_message_handler(delete_admin, state = BotStates.delete_admin_state)
    dp.register_message_handler(select_month, state = BotStates.change_subs_prices_state)
    dp.register_message_handler(change_1_moth_price, state = BotStates.moth_1_state)
    dp.register_message_handler(change_2_moth_price, state = BotStates.moth_2_state)
    dp.register_message_handler(change_3_moth_price, state = BotStates.moth_3_state)