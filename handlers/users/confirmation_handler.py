from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent
import asyncio


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
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

        })
        #res = await state.get_data()
        #print(res)
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
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
        streets_and_stations_data = (street_or_station[0], streets_and_stations_dict) if streets_and_stations_dict else ""

        searched_data = agent.get_all_cards(sell_or_rent, price_from, price_to, streets_or_stations = (street_or_station[0], streets_and_stations_dict), user_id = message.from_id, rooms = form_type) if streets_and_stations_data != "" else agent.get_all_cards(sell_or_rent, price_from, price_to, user_id = message.from_id, rooms = form_type)
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

        try:
            await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        except Exception as ex:
            print("|| NOT CRITICAL LAST MESSAGE ||")
            await asyncio.sleep(15)
            await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)

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