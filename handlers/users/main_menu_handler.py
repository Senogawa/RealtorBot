from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from database_methods import get_users_list
from database_methods import check_availability_users_in_database
from database_methods import run_command


async def start(message: types.Message, state: FSMContext):
    not_in_base = await check_availability_users_in_database(message, state)
    test_users = await get_users_list(True)
    test_users = test_users[0]
    test_users = [value[0] for value in test_users]


    if not_in_base and str(message.from_id) not in test_users :
        return

    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))
    form_type_board = Boards.form_type_board
    if str(message.from_id) in admins_list:
        form_type_board = Boards.form_type_board_admin

    await state.set_data({
            "form_type":list(),
            "form_type_names":list()

    })

    #Данные о оставшемся количестве поисков Проверка TODO 
    if str(message.from_id) in test_users: #TODO проверка на количество оставшихся поисков
        test_user_info = await run_command(f"SELECT * FROM test_users WHERE test_member_id='{message.from_id}'")
        test_user_info = test_user_info[0]
        if test_user_info['trials_finds_quantity'] == 0:
            await message.answer("У вас закончились пробные поиски!\nЖелаете приобрести подписку?", reply_markup = Boards.payments_or_test_trial_board)
            await BotStates.subscription_or_test_trial_state.set()
            return

        await message.answer(f"У вас осталось {test_user_info['trials_finds_quantity']} поисков\n\nВыберите тип объявления", reply_markup = form_type_board)

    else:
        await message.answer("Выберите тип объявления", reply_markup = form_type_board)

    del form_type_board
    await BotStates.form_type_state.set()



def register_all_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands = "start", state = "*")