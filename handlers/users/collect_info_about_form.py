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
        await state.set_data(
            {
                "form_type_multi":message.text,
                "form_type":list(),
                "form_type_names":list()
            }
        ) 
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

    form_type_dict: dict = await state.get_data()
    form_type_multi: str = form_type_dict["form_type_multi"]
    form_type: list = form_type_dict["form_type"]
    form_type_names: list = form_type_dict["form_type_names"]

    if message.text == "Выбрать все":
        form_type = list(card_states[form_type_multi][0]) + form_type
        form_type_names = list(card_states[form_type_multi][1].keys()) + form_type_names
        #print(form_type_names)
        await state.set_data({
            "form_type":set(form_type),
            "form_type_names":set(form_type_names)
        })
        res = await state.get_data()
        print(res)
        #TODO следующее состояние

    elif message.text == "Закончить с выбором параметров":

        await state.set_data({
            "form_type":set(form_type),
            "form_type_names":set(form_type_names)
        })
        res = await state.get_data() # tests
        print(res)
        #TODO переход в следующее состояние
        
    elif message.text not in Boards.all_form_answers:
        await message.answer("Пожалуйста воспользуйтесь клавиатурой")
        return

    elif message.text == "Назад":
        #TODO остановился здесь, в этой части - это последнее
        ...

    else:
        form_type.append(card_states[form_type_multi][1][message.text])
        form_type_names.append(message.text)
        await state.update_data({
            "form_type":form_type,
            "form_type_names":form_type_names
        })
        await message.answer("Выберите следующий параметр")

        res = await state.get_data()
        print(res) #tests
        return
        
    

def register_all_collecting_info_handlers(dp: Dispatcher):
    dp.register_message_handler(form_type_choice, state = BotStates.form_type_state)
    dp.register_message_handler(form_type_multi_choice, state = BotStates.multi_form_type_state)