from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent

async def street_or_station_input(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.update_data({
            "price_from": "",
            "price_to": ""
        })
        await message.answer(f"Введите ценовой диапазон\n1.Цена от: \n2.Цена до: \n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return
    elif message.text == "Не выбирать улицу":
        #TODO дублирование параметров в сообщении, подтверждение ввода
        await BotStates.confirmation_state.set()
        return
    streets_and_stations = agent.get_streets_and_stations_dict(message.text)
    print(streets_and_stations)
    return


def register_all_streets_or_stations_handlers(dp: Dispatcher):
    dp.register_message_handler(street_or_station_input, state = BotStates.street_or_station_input_state)