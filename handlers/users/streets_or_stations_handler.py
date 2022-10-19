from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent

async def street_or_station_input(message: types.Message, state: FSMContext):
    all_form_data = await state.get_data()
    print(all_form_data)
    if message.text == "Назад":
        await state.update_data({
            "price_from": "",
            "price_to": ""
        })
        await message.answer(f"Введите ценовой диапазон\n1.Цена от: \n2.Цена до: \n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return

    elif message.text == "Не выбирать улицу":
        #TODO дублирование параметров в сообщении, подтверждение ввода #TODO обязательно доделать
        await BotStates.confirmation_state.set()
        return

    streets_and_stations: dict = agent.get_streets_and_stations_dict(message.text)
    await state.update_data({
        "streets_and_stations_dict": streets_and_stations
    })
    streets_and_stations_board = types.ReplyKeyboardMarkup(resize_keyboard = True)
    streets: list = list(streets_and_stations["streets"].keys())
    stations: list = list(streets_and_stations["stations"].keys())
    for street in streets:
        streets_and_stations_board.add(street)

    for station in stations:
        streets_and_stations_board.add(station)

    streets_and_stations_board.add("Назад")

    await message.answer("Выберите улицу или метро из найденных вариантов", reply_markup = streets_and_stations_board)
    await BotStates.street_or_station_choice_state.set()
    return

async def street_or_station_choice(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.update_data({
            "streets_and_stations_dict": ""
        })
        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_or_station_input_state.set()
        return


def register_all_streets_or_stations_handlers(dp: Dispatcher):
    dp.register_message_handler(street_or_station_input, state = BotStates.street_or_station_input_state)
    dp.register_message_handler(street_or_station_choice, state = BotStates.street_or_station_choice_state)