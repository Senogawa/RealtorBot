from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from database_methods import get_users_list
from database_methods import check_availability_users_in_database


async def price_from(message: types.Message, state: FSMContext):

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    if message.text == "Не указывать ценовой диапазон":
        await state.update_data({
            "price_from": "",
            "price_to": ""
        })
        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_or_station_input_state.set()
        return

    elif message.text == "Назад":
        await message.answer("Аренда или продажа?", reply_markup = Boards.sell_or_rent_board)
        await state.update_data({
            "sell_or_rent": ...
        })
        await BotStates.sell_of_rent_state.set()
        return

    if message.text.isdigit():
        await state.update_data({
            "price_from": message.text
        })
        price_data = await state.get_data()
        price_from: str = price_data["price_from"]
        price_to: str = price_data["price_to"]

        await message.answer(f"Цена от: {price_from}\nЦена до: {price_to}\n\nВведите 'Цену до'", reply_markup = Boards.back_button_board)
        await BotStates.price_to_state.set()
        return

    await message.answer("Вводите только цифры")
    return

async def price_to(message: types.Message, state: FSMContext):

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    price_data = await state.get_data()
    price_from: str = price_data["price_from"]
    price_to: str = price_data["price_to"]

    if message.text == "Назад":
        await message.answer(f"Введите ценовой диапазон\n1.Цена от: {price_from}\n2.Цена до: {price_to}\n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await state.update_data({
            "price_from": ""
        })
        await BotStates.price_from_state.set()
        return

    if message.text.isdigit():
        if int(message.text) < int(price_from):
            await message.answer("'Цена до' должна быть больше, чем 'Цена от'")
            return

        await state.update_data({
            "price_to": message.text
        })
        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        res = await state.get_data()
        print(res)
        await BotStates.street_or_station_input_state.set()
        return

    await message.answer("Вводте только цифры")
    return

def register_all_price_from_to_handler(dp: Dispatcher):
    dp.register_message_handler(price_from, state = BotStates.price_from_state)
    dp.register_message_handler(price_to, state = BotStates.price_to_state)