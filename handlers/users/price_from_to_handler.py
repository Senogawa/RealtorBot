from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states


async def price_from(message: types.Message, state: FSMContext):
    if message.text == "Не указывать ценовой диапазон":
        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_of_station_input_state.set()
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

        await message.answer(f"Цена от:{message.text}\nЦена до:\n\nВведите 'Цену до'", reply_markup = Boards.back_button_board)
        await BotStates.price_to_state.set()
        return

    await message.answer("Вводите только цифры")
    return

async def price_to(message: types.Message, state: FSMContext):
    ...


def register_all_price_from_to_handler(dp: Dispatcher):
    dp.register_message_handler(price_from, state = BotStates.price_from_state)