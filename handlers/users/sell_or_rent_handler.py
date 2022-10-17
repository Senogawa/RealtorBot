from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states


async def sell_or_rent(message: types.Message, state: FSMContext):
    if message.text == "Аренда":
        await state.update_data({
            "sell_or_rent": False
        })
        await message.answer("Введите ценовой диапазон\n1.Цена от:\n2.Цена до\n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return

    elif message.text == "Продажа":
        await state.update_data({
            "sell_or_rent": True
        })
        await message.answer("Введите ценовой диапазон\n1.Цена от:\n2.Цена до\n\nВводите только цифры", reply_markup = Boards.price_from_to_board)
        await BotStates.price_from_state.set()
        return

    elif message.text == "Назад":
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()
        })
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    await message.answer("Пожалуйста воспользуйтесь клавиатурой")
    return



def register_all_sell_or_rent_handlers(dp: Dispatcher):
    dp.register_message_handler(sell_or_rent, state = BotStates.sell_of_rent_state)