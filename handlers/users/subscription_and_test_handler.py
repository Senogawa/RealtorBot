from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from database_methods import get_users_list
from database_methods import run_command
from loader import payments_or_test_trial_message
from middlewares.payments.payments_handler import products


async def paysubs_or_start_test_trial_main(message: types.Message, state: FSMContext):
    config = get_config_data()
    test_users = await get_users_list(True)
    test_users = test_users[1]

    if message.text == "Приобрести подписку":
        await message.answer("Есть несколько вариантов подписок, выберите для Вас самую удобную")
        await products(message)
        return

    elif message.text == "Воспользоваться тестовым периодом":
        trials_finds_quantity = config.get("smartagent").get("trials_finds_quantity")
        trials_finds_form_quantity = config.get("smartagent").get("trials_finds_form_quantity")

        if str(message.from_id) not in test_users:
            await run_command(f"INSERT INTO test_users(test_member_id, trials_finds_quantity, trials_finds_form_quantity) VALUES ('{message.from_id}', {trials_finds_quantity}, {trials_finds_form_quantity});", "SET")
            await message.answer("Тестовый период получен!\nВведите /start")
            return

        else:
            await message.answer("Вы уже получали тестовый период")
            return
    
    else:
        await message.answer("Воспользуйтесь клавиатурой")
        return


def register_all_subscription_and_test_handlers(dp: Dispatcher):
    dp.register_message_handler(paysubs_or_start_test_trial_main, state = BotStates.subscription_or_test_trial_state)


