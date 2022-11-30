from aiogram import types, Dispatcher
from loader import bot, bot_meta
from configparser import ConfigParser
from database_methods import run_command
import time
from states.state import BotStates
from keyboards.all_boards import Boards



def create_prices():
    cnf = ConfigParser()
    cnf.read("conf.ini")

    prices = [
        types.LabeledPrice("Подписка на 1 месяц", int(cnf.get("SUBSCRIPTIONS", "1_month"))),
        types.LabeledPrice("Подписка на 2 месяца", int(cnf.get("SUBSCRIPTIONS", "2_month"))),
        types.LabeledPrice("Подписка на 3 месяца", int(cnf.get("SUBSCRIPTIONS", "3_month"))),
        ]
    return prices

async def products(message: types.Message):
    prices = create_prices()
    await bot.send_invoice(message.chat.id, title = "Подписка на 1 месяц", description = "Позволяет пользоваться услугами бота в течении 1-го месяца", provider_token = bot_meta.payments_token, currency = "rub", need_email = True, prices = [prices[0]], start_parameter = "start_parameter", payload = "1-month")
    await bot.send_invoice(message.chat.id, title = "Подписка на 2 месяца", description = "Позволяет пользоваться услугами бота в течении 2-ух месяцев", provider_token = bot_meta.payments_token, currency = "rub", need_email = True, prices = [prices[1]], start_parameter = "start_parameter", payload = "2-month")
    await bot.send_invoice(message.chat.id, title = "Подписка на 3 месяца", description = "Позволяет пользоваться услугами бота в течении 3-ох месяцев", provider_token = bot_meta.payments_token, currency = "rub", need_email = True, prices = [prices[2]], start_parameter = "start_parameter", payload = "3-month")

async def pre_check(pre_check_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_check_query.id, True)

async def successful_payment(message: types.Message):
    print(time.time())
    print(message)
    if message.successful_payment.invoice_payload == "1-month":
        await run_command(f"INSERT INTO users(member_id, period) VALUES ('{message.from_id}', {int(time.time()) + 2592000});", "SET")

    if message.successful_payment.invoice_payload == "2-month":
        await run_command(f"INSERT INTO users(member_id, period) VALUES ('{message.from_id}', {int(time.time()) + 2592000 * 2});", "SET")

    if message.successful_payment.invoice_payload == "3-month":
        await run_command(f"INSERT INTO users(member_id, period) VALUES ('{message.from_id}', {int(time.time()) + 2592000 * 3});", "SET")
    
    await message.answer("Выберите тип объявления:", reply_markup = Boards.form_type_board)
    await BotStates.form_type_state.set()

def register_all_payments_handlers(dp:Dispatcher):
    #dp.register_message_handler(products, commands = "buy")
    dp.register_pre_checkout_query_handler(pre_check, lambda query: True)
    dp.register_message_handler(successful_payment, content_types = types.ContentTypes.SUCCESSFUL_PAYMENT)