from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent
from config_module import get_config_data
import asyncio
from database_methods import get_users_list
from database_methods import check_availability_users_in_database
from database_methods import run_command
import os


async def confirmation_options_and_start_parsing(message: types.Message, state: FSMContext):
    async def create_media(form: dict, message_about_form: str, message: types.Message):
        """
        Создание и заполнение медиа объекта
        """

        sended_message = False
        media = types.MediaGroup()
        i = 0
        for image in form["images"]: #добавление изображений
            print(len(form["images"]), i)
            if i  == 9:
                print(media)
                break
            if len(form["images"]) == 1:
                print("I AM HERE!")
                try:
                    await message.answer(message_about_form)
                except Exception as ex:
                    await asyncio.sleep(15)
                    print("|| NOT CRITICAL ||", ex)
                    await message.answer(message_about_form)

                try:
                    await message.answer_photo(types.InputFile(f"./parsingModule/images/No_photo.jpg"))
                except Exception as ex:
                    print("|| NOT CRITICAL ||", ex)
                    await asyncio.sleep(15)
                    await message.answer_photo(types.InputFile(f"./parsingModule/images/No_photo.jpg"))
                sended_message = True
                return (media, sended_message)

            media.attach_photo(types.InputFile(f"./parsingModule/images/{image}"))
            i += 1

        return (media, sended_message)

    not_in_base = await check_availability_users_in_database(message, state)
    if not_in_base:
        return

    test_users = await get_users_list(True)
    test_users = test_users[0]
    test_users = [value[0] for value in test_users]

    admins_list = get_config_data().get("admins").split(", ")
    admins_list.append(get_config_data().get("root"))
    if message.text == "Назад":
        form_data = await state.get_data()
        try:
            form_data.pop("street_or_station")
        except KeyError:
            pass

        try:
            form_data.pop("streets_and_stations_dict")
        except KeyError:
            pass
        
        await state.set_data(form_data)


        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_or_station_input_state.set()
        return

    elif message.text == "Указать параметры с самого начала":
        form_type_board = Boards.form_type_board
        if str(message.from_id) in admins_list:
            form_type_board = Boards.form_type_board_admin
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

        })
        #res = await state.get_data()
        #print(res)
        await message.answer("Выберите тип объявления", reply_markup = form_type_board)
        await BotStates.form_type_state.set()
        return

    elif message.text == "Начать поиск": #Отправка объявлений в бота
        await message.answer("Начинается сбор данных, ожидайте в течении 2-3 минут")
        form_data = await state.get_data()

        form_type = form_data["form_type"]
        price_from = form_data["price_from"]
        price_to = form_data["price_to"]
        sell_or_rent = form_data["sell_or_rent"]
        streets_and_stations_dict = form_data.get("streets_and_stations_dict")
        print(streets_and_stations_dict)
        street_or_station = form_data.get("street_or_station")
        streets_and_stations_data = (street_or_station[0], streets_and_stations_dict) if streets_and_stations_dict else False
        # print("--------")
        # print(streets_and_stations_data)
        # print(form_data)
        #os._exit(0)
        if str(message.from_id) in test_users:
            if streets_and_stations_data:
                searched_data = await asyncio.gather(asyncio.create_task(agent.get_all_cards(sell_or_rent, True, price_from, price_to, streets_or_stations = (street_or_station[0], streets_and_stations_dict), user_id = message.from_id, rooms = form_type, message = message)))

            else:
                 searched_data = await asyncio.gather(asyncio.create_task(agent.get_all_cards(sell_or_rent, True, price_from, price_to, user_id = message.from_id, rooms = form_type, message = message)))

        else:
            if streets_and_stations_data:
                print("with street")
                searched_data = await asyncio.gather(asyncio.create_task(agent.get_all_cards(sell_or_rent, price_from, price_to, streets_or_stations = (street_or_station[0], streets_and_stations_dict), user_id = message.from_id, rooms = form_type)))

            else:
                print("without street")
                searched_data = await asyncio.gather(asyncio.create_task(agent.get_all_cards(sell_or_rent, price_from, price_to, user_id = message.from_id, rooms = form_type)))

        searched_data = searched_data[0]
        if searched_data == None:
            await message.answer("По данным параметрам ничего не найдено")
            return
        #print(searched_data)
        await BotStates.static_state.set() #from actions
        for form in searched_data:
            #print(form["address_quick"])
            message_about_form = f"Название: {form['name']}\n\n"
            message_about_form += f"Жилая площадь: {form.get('living_area', 'Жилая площадь: Информация отсутствует')}\n\n" if form.get('living_area') != None else "Площадь кухни: Информация отсутствует\n\n"
            message_about_form += f"Площадь кухни: {form.get('kitchen_area', 'Площадь кухни: Информация отсутствует')}\n\n" if form.get('kitchen_area') != None else "Площадь кухни: Информация отсутствует\n\n"
            message_about_form += f"Цена: {form.get('price')} | {form.get('area_price')}\n\n" if sell_or_rent and "Земля" not in form.get("name") and "Доля" not in form.get("name") and "Комната" not in form.get("name") else f"Цена: {form.get('price')}\n\n"
            print(form.get("address_area"))
            if form["address_quick"] != "" and form.get('address_area') != None:
                message_about_form += f"Адресс: {form.get('address_area')} | {form.get('address_quick')}\n\n"

            elif form.get('address_area') == None and form.get("address_quick") != "":
                message_about_form += f"Адресс: {form.get('address_quick')}\n\n"

            elif form.get("address_quick") == "" and form.get("address_area") != None:
                message_about_form += f"Адресс: {form.get('address_area')}\n\n"

            #message_about_form += f"Адресс: {form.get('address_area')} | {form.get('address_quick')}\n\n" if form["address_quick"] != "" else f"Адресс: {form.get('address_area')}\n\n" if form.get('address_area') != None else ""
            message_about_form += f"Описание: {form.get('description')}\n\n"
            message_about_form += f"Метро: {form.get('metro').get('name')} {form.get('metro').get('lenght')}\n\n" if form.get("metro").get("name") != "" and form.get("metro").get("name") != None else ""
            message_about_form += f"Дата размещения: {form.get('date')}\n\n"
            #message_about_form += f"Номер телефона: {form.get('phone')[0]} {form.get('phone')[1]}\n" if form.get("phone")[1] != None else "Номер телефона: Данные не доступны"
            message_about_form += f"Номер телефона: {form.get('phone')[1]}\n" if form.get("phone")[1] != None else "Номер телефона: Данные не доступны"

            media, sended_message = await create_media(form, message_about_form, message)
            
            if sended_message: # если сообщение было отправлено
                await asyncio.sleep(1)
                continue
                
            try:
                await message.answer(message_about_form, parse_mode = "HTML") #TODO обход защиты от флуда
            except Exception as ex:
                print("|| NOT CRITICAL MESSAGE||\n", ex)
                await asyncio.sleep(15)
                await message.answer(message_about_form, parse_mode = "HTML")

            try:
                await message.answer_media_group(media)
            except Exception as ex:
                print("|| NOT CRITICAL MEDIA ||\n", ex)
                media, sended_message = await create_media(form, message_about_form, message)
                await asyncio.sleep(15)
                await message.answer_media_group(media)
                

            agent.delete_all_photo(form["images"])
            await asyncio.sleep(1)

        form_type_board = Boards.form_type_board
        if str(message.from_id) in admins_list:
            form_type_board = Boards.form_type_board_admin

        if str(message.from_id) in test_users:
            test_user_info = await run_command(f"SELECT * FROM test_users WHERE test_member_id='{message.from_id}'")
            test_user_info = test_user_info[0]
            await run_command(f"UPDATE test_users SET trials_finds_quantity={test_user_info['trials_finds_quantity'] - 1} WHERE test_member_id='{message.from_id}'", "SET")
            test_user_trials_finds_quantity = test_user_info['trials_finds_quantity'] - 1

            if test_user_trials_finds_quantity == 0:
                    await run_command(f"DELETE FROM test_users WHERE test_member_id='{message.from_id}'", "SET")
                    await run_command(f"INSERT INTO users_used_trials_period(user_id) VALUES ('{message.from_id}')", "SET")

        try:
            if str(message.from_id) in test_users: #TODO проверка на количество оставшихся поисков
                if test_user_trials_finds_quantity == 0:
                    await message.answer("У вас закончились пробные поиски!\nЖелаете приобрести подписку?", reply_markup = Boards.payments_or_test_trial_board)
                    await BotStates.subscription_or_test_trial_state.set()
                    await state.set_data({
                        "form_type":list(),
                        "form_type_names":list()
                        })
                    return

                await message.answer(f"У вас осталось {test_user_trials_finds_quantity} поисков\n\nВыберите тип объявления", reply_markup = form_type_board)

            else:
                await message.answer("Выберите тип объявления", reply_markup = form_type_board)

        except Exception as ex:
            print("|| NOT CRITICAL LAST MESSAGE ||")
            await asyncio.sleep(15)
            if str(message.from_id) in test_users: #TODO проверка на количество оставшихся поисков
                if test_user_trials_finds_quantity == 0:
                    await message.answer("У вас закончились пробные поиски!\nЖелаете приобрести подписку?", reply_markup = Boards.payments_or_test_trial_board)
                    await BotStates.subscription_or_test_trial_state.set()
                    await state.set_data({
                        "form_type":list(),
                        "form_type_names":list()
                        })
                    return

                await message.answer(f"У вас осталось {test_user_trials_finds_quantity} поисков\n\nВыберите тип объявления", reply_markup = form_type_board)

            else:
                await message.answer("Выберите тип объявления", reply_markup = form_type_board)

        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

            })
        await BotStates.form_type_state.set()
        return

    await message.answer("Пожалуйста воспользуйтесь клавиатурой")
    return
    



def register_all_confirmation_handlers(dp: Dispatcher):
    dp.register_message_handler(confirmation_options_and_start_parsing, state = BotStates.confirmation_state)