from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from config_module import get_config_data
from database_methods import get_users_list
from database_methods import check_availability_users_in_database


async def sell_or_rent(message: types.Message, state: FSMContext):

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    price_data = await state.get_data()
    price_from: str = price_data["price_from"]
    price_to: str = price_data["price_to"]
    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))

    if message.text == "Аренда":
        await state.update_data({
            "sell_or_rent": False
        })
        await message.answer(f"Введите ценовой диапазон\n1.Цена от: {price_from}\n2.Цена до: {price_to}\n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return

    elif message.text == "Продажа":
        await state.update_data({
            "sell_or_rent": True
        })
        await message.answer(f"Введите ценовой диапазон\n1.Цена от: {price_from}\n2.Цена до: {price_to}\n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return

    elif message.text == "Назад":
        form_type_board = Boards.form_type_board
        if str(message.from_id) in admins_list:
            form_type_board = Boards.form_type_board_admin

        await state.set_data({
            "form_type":list(),
            "form_type_names":list()
        })
        await message.answer("Выберите тип объявления", reply_markup = form_type_board)
        await BotStates.form_type_state.set()
        return

    await message.answer("Пожалуйста воспользуйтесь клавиатурой")
    return



def register_all_sell_or_rent_handlers(dp: Dispatcher):
    dp.register_message_handler(sell_or_rent, state = BotStates.sell_of_rent_state)