from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states

async def form_type_choice(message: types.Message, state: FSMContext):
    """
    Получение информации о типе объявления
    """

    if message.text == "Квартира" or message.text == "Коммерческая недвижимость":
        await state.set_data({"form_type_multi":message.text})
        if message.text == "Квартира":
            board = Boards.form_type_flat

        elif message.text == "Коммерческая недвижимость":
            board = Boards.form_type_commercian

        await message.answer("Выберите подтип", reply_markup = board)
        await BotStates.multi_form_type_state.set()
        return

    elif message.text not in Boards.all_form_answers:
        await message.answer("Пожалуйста воспользуйтесь клавиатурой")
        return #TODO остановился здесь

async def form_type_multi_choice(message: types.Message, state: FSMContext):
    """
    Выбор подъобьявления из Квартира или Коммерческая недвижимость
    """

    form_type = await state.get_data()
    form_type = form_type["form_type_multi"]
    await state.reset_data()

    if message.text == "Выбрать все":
        await state.set_data({"form_type":(form_type, card_states[form_type][0])})
        #TODO следующее состояние
    else:
        await state.set_data({"form_type":(message.text, card_states[form_type][1][message.text])})
    res = await state.get_data()
    print(res)

def register_all_collecting_info_handlers(dp: Dispatcher):
    dp.register_message_handler(form_type_choice, state = BotStates.form_type_state)
    dp.register_message_handler(form_type_multi_choice, state = BotStates.multi_form_type_state)