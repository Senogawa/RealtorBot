import asyncpg
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from config_module import get_config_data
from loader import payments_or_test_trial_message

async def run_command(query: str, get_or_change: str = "GET"):
    """
    Выполнить команду в базе и вернуть результат
    """
    pool = await asyncpg.create_pool("postgresql://dante@localhost/realtorbot")

    if get_or_change == "GET":
        res = await pool.fetch(query)
        await pool.close()
        return res

    elif get_or_change == "SET":
        await pool.execute(query)
        await pool.close()
        return None

async def get_users_list(test: bool = False):
    pool = await asyncpg.create_pool("postgresql://dante@localhost/realtorbot")

    if test:
        res = await pool.fetch("SELECT * FROM test_users;")
        res_processed = [(value["test_member_id"], value["trials_finds_quantity"]) for value in res]
        res = await pool.fetch("SELECT * FROM users_used_trials_period")
        res_processed_two = [value["user_id"] for value in res]
        await pool.close()
        return (res_processed, res_processed_two)
        

    else:
        res = await pool.fetch("SELECT * FROM users;")
        res_processed = [value["member_id"] for value in res]

        await pool.close()
        return res_processed
    
async def check_availability_users_in_database(message: types.Message, state: FSMContext):
    users = await get_users_list()
    test_users = await get_users_list(True)
    test_users = [value[0] for value in test_users[0]]
    config = get_config_data()
    if str(message.from_id) == config.get("root"):
        return False

    if str(message.from_id) not in users and str(message.from_id) not in config.get("admins").split(", ") and str(message.from_id) not in test_users:
        await message.answer(payments_or_test_trial_message, reply_markup = Boards.payments_or_test_trial_board)
        await BotStates.subscription_or_test_trial_state.set()
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

            })
        return True

    return False

    


