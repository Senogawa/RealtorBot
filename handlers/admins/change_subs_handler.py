from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import set_config_parameter
from config_module import create_config_data_message
from config_module import get_config_data



async def select_month(message: types.Message, state: FSMContext):
    config_data = get_config_data()

    if str(message.from_id) != config_data.get("root"):
        await message.answer("У вас нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    if message.text == "1 месяц":
        await message.answer("Введите стоимость", reply_markup = Boards.back_button_board)
        await BotStates.moth_1_state.set()
        return

    if message.text == "2 месяца":
        await message.answer("Введите стоимость", reply_markup = Boards.back_button_board)
        await BotStates.moth_2_state.set()
        return

    if message.text == "3 месяца":
        await message.answer("Введите стоимость", reply_markup = Boards.back_button_board)
        await BotStates.moth_3_state.set()
        return

    if message.text == "Назад":
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    await message.answer("Воспользуйтесь клавиатурой")
    return

async def change_1_moth_price(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    if str(message.from_id) != config_data.get("root"):
        await message.answer("У вас нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    if message.text.isdigit():
        set_config_parameter("SUBSCRIPTIONS", "1_month", str(int(message.text)*100))
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    if message.text == "Назад":
        await message.answer("Выберите, какую стоимость изменить?", reply_markup = Boards.root_payments_board)
        await BotStates.change_subs_prices_state.set()
        return

    await message.answer("Это должны быть цифры")
    return

async def change_2_moth_price(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    if str(message.from_id) != config_data.get("root"):
        await message.answer("У вас нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    if message.text.isdigit():
        set_config_parameter("SUBSCRIPTIONS", "2_month", str(int(message.text)*100))
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    if message.text == "Назад":
        await message.answer("Выберите, какую стоимость изменить?", reply_markup = Boards.root_payments_board)
        await BotStates.change_subs_prices_state.set()
        return

    await message.answer("Это должны быть цифры")
    return

async def change_3_moth_price(message: types.Message, state: FSMContext):
    config_data = get_config_data()
    if str(message.from_id) != config_data.get("root"):
        await message.answer("У вас нет доступа к этому меню!")
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    if message.text.isdigit():
        set_config_parameter("SUBSCRIPTIONS", "3_month", str(int(message.text)*100))
        await message.answer(create_config_data_message()[1], reply_markup = Boards.root_board, parse_mode = "HTML")
        await BotStates.admin_menu_state.set()
        return

    if message.text == "Назад":
        await message.answer("Выберите, какую стоимость изменить?", reply_markup = Boards.root_payments_board)
        await BotStates.change_subs_prices_state.set()
        return

    await message.answer("Это должны быть цифры")
    return