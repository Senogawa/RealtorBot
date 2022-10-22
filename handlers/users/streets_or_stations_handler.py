from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent


def create_message(form_data: dict):
    """
    Создание сообщения о общих данных поиска
    """

    message = "Выбранные параметры:\n\n"
    form_type_names = form_data.get("form_type_names")
    price_from = form_data.get("price_from")
    price_to = form_data.get("price_to")
    sell_or_rent = form_data.get("sell_or_rent")
    street_or_station = form_data.get("street_or_station", "Глобальный поиск")
    message += "Тип объявления - "
    for name in form_type_names:
        message += name + ", "
    message = message[0:-2] + ".\n\n"
    message += f"Ценовой диапазон - {price_from + ' - ' + price_to if price_from != '' else 'Не указан'}.\n\n"
    message += f"Аренда или продажа - {'Продажа' if sell_or_rent else 'Аренда'}\n\n"
    message += f"Улица или метро - {street_or_station[0] if street_or_station != 'Глобальный поиск' else street_or_station}\n\n"
    message += f"|INFO| Внимание, бот присылает объявления отдельными сообщениями, этот процесс нельзя остановить, вы уверены что хотите начать поиск? |INFO|"
    return message

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
        await message.answer(create_message(all_form_data), reply_markup = Boards.confirmation_board)
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

    streets_and_stations_dict = await state.get_data()
    print(streets_and_stations_dict)
    streets_and_stations_dict = streets_and_stations_dict["streets_and_stations_dict"]
    streets_and_stations = {name:value for name, value in streets_and_stations_dict["streets"].items()}

    for name, value in streets_and_stations_dict["stations"].items():
        streets_and_stations[name] = value

    if streets_and_stations.get(message.text) == None:
        await message.answer("Нет такого варианта, пожалуйста воспользуйтесь клавиатурой")
        return

    await state.update_data({
        "street_or_station":(message.text, streets_and_stations[message.text]),
        "streets_and_stations_dict": ""
    })

    form_data = await state.get_data()
    await message.answer(create_message(form_data), reply_markup = Boards.confirmation_board)
    await BotStates.confirmation_state.set()



def register_all_streets_or_stations_handlers(dp: Dispatcher):
    dp.register_message_handler(street_or_station_input, state = BotStates.street_or_station_input_state)
    dp.register_message_handler(street_or_station_choice, state = BotStates.street_or_station_choice_state)