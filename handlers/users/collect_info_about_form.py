from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from config_module import get_config_data
from config_module import create_config_data_message
from database_methods import get_users_list
from database_methods import check_availability_users_in_database

def create_user_text(form_type_names: list):
    """
    Создание подтверждающего текста для пользователя
    """

    form_data_text = "Выбранные параметры:\n"
    for text in form_type_names:
        form_data_text = form_data_text + f"{text}\n"
    
    form_data_text = form_data_text + "\nВсе верно?"

    return form_data_text

async def form_type_choice(message: types.Message, state: FSMContext):
    """
    Получение информации о типе объявления
    """

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    form_data: dict = await state.get_data()
    form_type: list = list(form_data["form_type"])
    form_type_names: list = list(form_data["form_type_names"])
    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))

    if message.text == "Квартира" or message.text == "Коммерческая недвижимость":
        await state.update_data(
            {
                "form_type_multi":message.text
            }
        ) 
        if message.text == "Квартира":
            board = Boards.form_type_flat

        elif message.text == "Коммерческая недвижимость":
            board = Boards.form_type_commercian

        await message.answer("Выберите подтип", reply_markup = board)
        await BotStates.multi_form_type_state.set()
        return

    elif message.text == "Закончить с выбором параметров":
        if len(form_type) == 0:
            await message.answer("Oops!\nВы должны выбрать хотя бы 1 параметр")
            return

        await state.set_data({
            "form_type":set(form_type),
            "form_type_names":set(form_type_names)
        })
        res = await state.get_data() # tests
        print(res)


        await message.answer(create_user_text(set(form_type_names)), reply_markup = Boards.accept_form_data_board)
        await BotStates.accept_form_type_state.set()
        return
        #TODO запрос о подтверждении

    elif message.text == "Выбрать все объявления":
        form_type = [item for item in card_states.values() if type(item) is not tuple and item.isdigit()]
        form_type.remove("4")
        form_type.remove("3")
        form_type = form_type + list(card_states["Квартира"][0]) + list(card_states["Коммерческая недвижимость"][0])

        form_type_names = [item for item in card_states.keys()]
        form_type_names.remove("Аренда")
        form_type_names.remove("Продажа")
        form_type_names = form_type_names + list(card_states["Квартира"][1].keys()) + list(card_states["Коммерческая недвижимость"][1].keys())

        await state.set_data({
            "form_type":form_type,
            "form_type_names":form_type_names
        })

        await message.answer(create_user_text(form_type_names), reply_markup = Boards.accept_form_data_board)
        await BotStates.accept_form_type_state.set()
        return

    elif message.text == "Настройки администратора" and str(message.from_id) in admins_list:
        admin_board = Boards.admin_board
        if str(message.from_id) == get_config_data().get("root"):
            admin_board = Boards.root_board

        message_text = create_config_data_message()[1]
        await message.answer(message_text, parse_mode = "HTML", reply_markup = admin_board)
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

            })
        await BotStates.admin_menu_state.set()
        return

    elif message.text not in Boards.all_form_answers:
        await message.answer("Пожалуйста воспользуйтесь клавиатурой")
        return #TODO остановился здесь

    
    form_type.append(card_states[message.text])
    form_type_names.append(message.text)
    await state.update_data({
        "form_type":form_type,
        "form_type_names":form_type_names
    })

    await message.answer("Выберите следующий параметр")
    res = await state.get_data()
    print(res)
    return


async def form_type_multi_choice(message: types.Message, state: FSMContext):
    """
    Выбор подъобьявления из Квартира или Коммерческая недвижимость
    """

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    form_type_dict: dict = await state.get_data()
    print(form_type_dict)
    form_type_multi: str = form_type_dict["form_type_multi"]
    form_type: list = list(form_type_dict["form_type"])
    form_type_names: list = list(form_type_dict["form_type_names"])
    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))

    if message.text == "Выбрать все":
        form_type = list(card_states[form_type_multi][0]) + form_type
        form_type_names = list(card_states[form_type_multi][1].keys()) + form_type_names
        #print(form_type_names)
        await state.update_data({
            "form_type":set(form_type),
            "form_type_names":set(form_type_names)
        })
        res = await state.get_data()
        print(res)
        form_type_board = Boards.form_type_board
        if str(message.from_id) in admins_list:
            form_type_board = Boards.form_type_board_admin
        await message.answer("Выберите следующий параметр", reply_markup = form_type_board)
        await BotStates.form_type_state.set()
        return

    elif message.text == "Закончить с выбором параметров":
        if len(form_type) == 0:
            await message.answer("Oops!\nВы должны выбрать хотя бы 1 параметр")
            return

        await state.set_data({
            "form_type":set(form_type),
            "form_type_names":set(form_type_names)
        })
        res = await state.get_data() # tests
        print(res)
        await message.answer(create_user_text(set(form_type_names)), reply_markup = Boards.accept_form_data_board)
        await BotStates.accept_form_type_state.set()
        return

    elif message.text == "Назад":
        form_type_board = Boards.form_type_board
        if str(message.from_id) in admins_list:
            form_type_board = Boards.form_type_board_admin

        await message.answer("Выберите тип объявления", reply_markup = form_type_board)
        await BotStates.form_type_state.set()
        del form_type_board
        return

    elif message.text not in Boards.all_form_answers:
        await message.answer("Пожалуйста воспользуйтесь клавиатурой")
        return


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