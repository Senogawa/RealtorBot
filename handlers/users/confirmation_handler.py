from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states


async def confirmation_options_and_start_parsing(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        form_data = await state.get_data()
        try:
            form_data.pop("street_or_station")
        except KeyError:
            pass

        try:
            form_data.pop("streets_and_stations_dict")
        except KeyError:
            pass
        
        await state.set_data(form_data)

        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_or_station_input_state.set()
        return



def register_all_confirmation_handlers(dp: Dispatcher):
    dp.register_message_handler(confirmation_options_and_start_parsing, state = BotStates.confirmation_state)