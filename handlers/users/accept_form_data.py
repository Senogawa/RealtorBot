from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from loader import bot_meta


async def accept(message: types.Message, state: FSMContext):
    if message.text == "Все верно":
        await state.update_data({
            "price_from": "",
            "price_to": ""
        })
        await message.answer("Аренда или продажа?", reply_markup = Boards.sell_or_rent_board)
        await BotStates.sell_of_rent_state.set()
        return
        
    elif message.text == "Заполнить заново":
        form_type_board = Boards.form_type_board
        if str(message.from_id) in bot_meta.admins:
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


    



def register_all_accept_form_data_handlers(dp: Dispatcher):
    dp.register_message_handler(accept, state = BotStates.accept_form_type_state)