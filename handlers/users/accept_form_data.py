from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states


async def accept(message: types.Message, state: FSMContext):
    if message.text == "Все верно":
        await message.answer("Аренда или продажа?", reply_markup = Boards.sell_or_rent_board)
        await BotStates.sell_of_rent_state.set()
        return
        
    elif message.text == "Заполнить заново":
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()
        })
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    await message.answer("Пожалуйста воспользуйтесь клавиатурой")
    return


    



def register_all_accept_form_data_handlers(dp: Dispatcher):
    dp.register_message_handler(accept, state = BotStates.accept_form_type_state)